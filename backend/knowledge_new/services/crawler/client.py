import os.path
from http.client import HTTPException
from services.crawler.parser import HtmlParser
from config.settings import settings
import  requests


class KnowledgeApiClient:
    """主要提供一个方法 获取网络知识"""

    @staticmethod
    def  fetch_knowledge_content(knowledge_no:str)->str:
        """根据知识库编号 获取联想知识库内容(data部分)"""
        try:
            

            
            knowledge_base_url=f"{settings.KNOWLEDGE_BASE_URL}/knowledgeapi/api/knowledge/knowledgeDetails"

            
            params={"knowledgeNo":knowledge_no}

            
            response=requests.get(url=knowledge_base_url, params=params,timeout=10)
            response.raise_for_status()

            
            response_dict=response.json()
            
            return  response_dict['data']
        except HTTPException as  e:
            raise HTTPException(f"发送知识库请求失败:{e}")


if __name__ == '__main__':

    knowledge_content=KnowledgeApiClient.fetch_knowledge_content(knowledge_no=1)

    print(f"知识库1数据内容:\n{knowledge_content}")

    parser=HtmlParser()
    md_content=parser.parse_html_to_markdown(1,knowledge_content)

    file_name_path=os.path.dirname(__file__)

    file_name=os.path.join(file_name_path,"test_01.md")

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(md_content)






