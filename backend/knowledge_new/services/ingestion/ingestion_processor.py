import os.path
from wsgiref.validate import validator

from repositories.vector_store_repository import VectorStoreRepository
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import  RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata
from  utils.markdown_utils import MarkDownUtils
import  logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

class IngestionProcessor:
    """
    文档摄入类：（摄入：加载、切分、存储）
    """

    def __init__(self):

        self.vector_store = VectorStoreRepository()
        self.document_spliter=RecursiveCharacterTextSplitter(
            chunk_size=1500,  
            chunk_overlap=200,
            separators=[
                "\n## ",
                "\n**"
                "\n\n",
                "\n",
                " ",
                ""
            ]
        )

    def ingest_file(self, md_path: str) -> int:
        """
        文档完整操作
        包含阶段：文件的加载->文档的切割->文档的存储
        Args:
            md_path:文件的路径

        Returns:
          int: 保存成功的文档数
        """

        
        
        try:
            text_loader = TextLoader(file_path=md_path,encoding="utf-8")
            
            documents = text_loader.load()
        except Exception as e:
            logger.error(f"文件：{md_path}没有加载到,原因:{str(e)}")
            raise Exception(f"文件：{md_path}没有加载到,原因:{str(e)}")
        
        
        
        


        for doc  in documents:
            doc.metadata['title']=MarkDownUtils.extract_title(md_path)



        
        
        
        

        final_document_chunks=[]
        for doc in documents:
            if len(doc.page_content)<3000:  
                
                final_document_chunks.append(doc)
            else:
                documents_chunks_list = self.document_spliter.split_documents(documents)
                
                
                for  document_chunk in documents_chunks_list:

                    
                    md_path=document_chunk.metadata['source']

                    title=os.path.basename(md_path)

                    
                    document_chunk.page_content=f"文档来源:{title}\n{document_chunk.page_content}"
                final_document_chunks.extend(documents_chunks_list)


        
        clean_documents_chunks=filter_complex_metadata(final_document_chunks)

        
        valid_documents_chunks=[document for document in  clean_documents_chunks if document.page_content.strip()]

        if not valid_documents_chunks:
            logger.error("切分后的文档块没有任何的内容")
            return 0

        
        total_documents_chunks=self.vector_store.add_documents(valid_documents_chunks)


        
        return total_documents_chunks


if __name__ == '__main__':
    
    
    
    
    

    

    
    
    
    
    
    
    
    

    import argparse

    parser = argparse.ArgumentParser(description="Ingest a Markdown document.")
    parser.add_argument("md_path", help="Path to the Markdown document")
    args = parser.parse_args()
    md_path = os.path.abspath(args.md_path)
    if not os.path.isfile(md_path):
        parser.error(f"File not found: {md_path}")

    ingest_processor=IngestionProcessor()
    ingest_processor.ingest_file(md_path)
    







