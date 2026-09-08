import logging
import jieba
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from typing import List, Dict, Any
from langchain_core.documents import Document
from repositories.vector_store_repository import VectorStoreRepository
from services.ingestion.ingestion_processor import IngestionProcessor
from utils.markdown_utils import MarkDownUtils
from config.settings import settings
from sklearn.metrics.pairwise import cosine_similarity


class RetrievalService:
    """
    负责检索的类（检索器）
    RAG:（小块：越小越好【小（无线小）】）文本嵌入模型  （完整信息：越大越大【不能无限大】）文本语言模型====准 原文档（大）--->1.小块（子） 2.稍微大一点的块（整个文档）【父】---留一个保留关系：穿针引线思想（父文档召回）
    """

    def __init__(self):
        self.chroma_vector = VectorStoreRepository()
        self.spliter = IngestionProcessor()

    def rough_ranking(self, user_query, mds_metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
         对标题进行粗排
         基于jieba进行标题的分词匹配
        Args:
            user_query: 用户的问题
            mds_metadata: 所有md的元数据（标题【title】，路径【path】）

        Returns:
            List[Dict[str,Any]]:所有md的元数据 （标题【title】，路径【path】，标题粗排得分【rough_score】）
        """

        
        if not user_query:
            return []
        ROUGHIN_WORD_WEIGHT = 0.7

        
        for md_metadata in mds_metadata:
            
            md_metadata_title = md_metadata['title']

            
            if not md_metadata_title and not md_metadata_title.strip():
                continue
            
            
            user_query_char = set(user_query)
            md_metadata_title_char = set(md_metadata_title)
            unique_char = user_query_char | md_metadata_title_char
            char_score = len(user_query_char & md_metadata_title_char) / len(unique_char) if len(unique_char) > 0 else 0

            
            user_query_word = set(jieba.lcut(user_query))
            md_metadata_title_word = set(jieba.lcut(md_metadata_title))
            unique_word = user_query_word | md_metadata_title_word
            word_score = len(user_query_word & md_metadata_title_word) / len(unique_word) if len(unique_word) > 0 else 0

            
            roughing_score = word_score * ROUGHIN_WORD_WEIGHT + char_score * (1 - ROUGHIN_WORD_WEIGHT)

            md_metadata['roughing_score'] = float(roughing_score)

        
        return sorted(mds_metadata, key=lambda x: x['roughing_score'], reverse=True)[:50]

    def fine_ranking(self, user_query: str, rough_mds_metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
         对标题进行精排
         基于嵌入模型相似性以及cosine_similarity()
        Args:
            user_query: 用户当前问题
            rough_mds_metadata: 粗排后的md元数据

        Returns:
            List[Dict[str, Any]]: 带精排分数的元数据
        """

        
        if not rough_mds_metadata:
            return []

        

        
        query_embedding = self.chroma_vector.embedd_document(user_query)

        
        roughing_title = [md_metadata['title'] for md_metadata in rough_mds_metadata]

        
        roughing_title_embeddings = self.chroma_vector.embedd_documents(roughing_title)

        
        
        
        similarity = cosine_similarity([query_embedding], roughing_title_embeddings).flatten()

        
        ROUGH_HEIGHT = 0.3
        SIM_HEIGHT = 0.7
        for index, md_metadata in enumerate(rough_mds_metadata):

            
            sim = similarity[index]
            if sim < 0:
                sim = 0
            
            roughing_score = md_metadata['roughing_score']

            
            final_score = roughing_score * ROUGH_HEIGHT + sim * SIM_HEIGHT

            
            md_metadata['sim_score'] = sim
            md_metadata['final_score'] = final_score

        
        relevant_metadata = [
            metadata
            for metadata in rough_mds_metadata
            if metadata['roughing_score'] >= settings.TITLE_ROUGH_SCORE_THRESHOLD
        ]
        sim_mds_metadata = sorted(relevant_metadata, key=lambda x: x['final_score'], reverse=True)[:5]

        
        return sim_mds_metadata

    def retrieval(self, user_question: str) -> List[Document]:
        """
         核心检索方法（检索器的入口）
        Args:
            user_question: 用户输入的问题

        Returns:
           List[Document]: 返回指定Top-N个相似性文档列表
        """

        
        based_vector_candidates = self._search_based_vector(user_question)

        
        based_title_candidates = self._search_based_title(user_question)

        
        total_candidates = based_vector_candidates + based_title_candidates

        
        unique_candidates = self._deduplicate(total_candidates)

        
        top_documents = self._reranking(unique_candidates, user_question)

        
        return top_documents

    def _search_based_vector(self, user_question: str) -> List[Document]:
        """
        第一路检索
        基于语义相似度检索

        Args:
            user_question: 用户输入的问题

        Returns:
            List[Document]： Top-N个相似的文档列表

        """
        
        documents_with_score = self.chroma_vector.search_similarity_with_score(user_question)

        
        based_vector_candidates = []
        for document, distance in documents_with_score:
            if distance <= settings.VECTOR_DISTANCE_THRESHOLD:
                based_vector_candidates.append(document)
        return based_vector_candidates

    def _search_based_title(self, user_query: str) -> List[Document]:
        """
         第二路检索
         基于标题的关键词匹配检索
        Args:
            user_query: 用户输入的问题

        Returns:
            List[Document]: Top-N个相似的文档列表

        """

        
        mds_metadata = MarkDownUtils.collect_md_metadata(settings.MD_FOLDER_PATH)

        
        
        
        rough_mds_metadata = self.rough_ranking(user_query, mds_metadata)
        fine_mds_metadata = self.fine_ranking(user_query, rough_mds_metadata)

        

        based_title_candidates = []
        for fine_md_metadata in fine_mds_metadata:
            try:
                
                with open(fine_md_metadata['path'], "r", encoding="utf-8") as f:
                    content = f.read().strip()
                
                
                if len(content) < 3000:
                    
                    doc = Document(page_content=content, metadata={
                        "path": fine_md_metadata['path'],
                        "title": fine_md_metadata['title'],
                    })
                    based_title_candidates.append(doc)
                
                else:
                    doc_chunks = self._deal_long_title_content(content, fine_md_metadata, user_query)
                    based_title_candidates.extend(doc_chunks)  
            except Exception as e:

                logger.error(f"打开文件失败:{e}")
                return []
        

        return based_title_candidates

    def _deduplicate(self, total_candidates: List[Document]) -> List[Document]:
        """
         对合并后的文档列表去重
         用set()集合去重（(title,内容的前【100】个字符)）-->key
        Args:
            total_candidates: 合并的文档列表

        Returns:
            List[Document]：唯一的文档列表
        """

        if not total_candidates:
            return []

        
        seen = set()
        unique_candidates = []

        
        for document in total_candidates:
            
            clean_content = re.sub(r'^文档来源:.*?(?=(\n|#))', '', document.page_content, flags=re.DOTALL).strip()
            key = (document.metadata['title'], clean_content[:100])
            if key not in seen:
                seen.add(key)
                unique_candidates.append(document)

        
        return unique_candidates

    def _reranking(self, unique_candidates: List[Document], user_question: str) -> List[Document]:
        """
         重新计算打分&&排序
         第二路长文档已经进行了cosine_similarity()的计算（无需在次打分）
         对第一路的文档和第二路的短文档进行重新计算

        Args:
            unique_candidates: 唯一的候选文档列表
            user_question: 用户输入的问题

        Returns:
            List[Document]: 最终指定Top-N的文档列表

        """

        
        if not unique_candidates:
            return []

        need_embedding_docs = []
        need_embedding_candidates_indices = []
        score_doc = []

        
        for candidate_index, unique_candidate in enumerate(unique_candidates):
            
            
            if "chunk_index" in unique_candidate.metadata and "similarity" in unique_candidate.metadata:
                score_doc.append((unique_candidate, unique_candidate.metadata['similarity']))
            
            else:
                need_embedding_docs.append(unique_candidate)
                need_embedding_candidates_indices.append(candidate_index)

        
        if need_embedding_docs:
            
            query_embedding = self.chroma_vector.embedd_document(user_question)

            
            embedding_docs_content = ["文档来源:" + doc.metadata['title'] + doc.page_content for doc in
                                      need_embedding_docs]
            
            doc_embeddings = self.chroma_vector.embedd_documents(embedding_docs_content)

            
            similarity = cosine_similarity([query_embedding], doc_embeddings).flatten()

            
            for idx, candidate_index in enumerate(need_embedding_candidates_indices):
                score_doc.append((unique_candidates[candidate_index], similarity[idx]))

        
        sorted_docs = sorted(score_doc, key=lambda x: x[1], reverse=True)

        
        return [doc for doc, _ in sorted_docs[:2]]

    def _deal_long_title_content(self, content: str, fine_md_metadata: Dict[str, Any], user_query: str) -> List[
        Document]:
        """
         处理标题对应的长文本
         切分-->文档块--->算文档块和问题的相似度
        Args:
            content: 长文本
            fine_md_metadata: 长文本对应的元数据
            user_query: 用户的问题

        Returns:
            List[Document]: 和问题相似的文档块（chunk）
        """

        
        chunks = self.spliter.document_spliter.split_text(content)

        
        doc_chunks_title = fine_md_metadata['title']

        
        doc_chunks_inject_title = [f"文档来源:{doc_chunks_title}" + doc_chunk for doc_chunk in chunks]

        
        query_embedding = self.chroma_vector.embedd_document(user_query)

        
        doc_chunk_embeddings = self.chroma_vector.embedd_documents(doc_chunks_inject_title)

        
        doc_chunks_similarity = cosine_similarity([query_embedding], doc_chunk_embeddings).flatten()

        
        top_doc_chunks_indices = doc_chunks_similarity.argsort()[-3:][::-1]

        
        docs = []
        for i, chunk_idx in enumerate(top_doc_chunks_indices):
            doc = Document(
                page_content=doc_chunks_inject_title[chunk_idx],  
                metadata={
                    "path": fine_md_metadata['path'],
                    "title": fine_md_metadata['title'],
                    "chunk_index:": int(chunk_idx),
                    "similarity": float(doc_chunks_similarity[chunk_idx])
                }
            )
            docs.append(doc)

        return   docs


if __name__ == '__main__':
    retrival_service = RetrievalService()

    
    
    
    
    
    
    
    

    
    
    
    
    
    
    result = retrival_service.retrieval("手机、平板上的画面能无线传输到电视上播放吗") 

    for r in result:
        print(r)
