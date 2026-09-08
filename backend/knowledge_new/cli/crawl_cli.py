import os
import time
from  services.crawler.client import KnowledgeApiClient
from  services.crawler.parser import HtmlParser
from  utils.text_utils import  TextUtils
from  config.settings import  settings
from  repositories.file_repository import FileRepository


def  main():

    success=0
    fail=0
    for  i in range(1000):
        print(f"[{i+1}/1000] 获取KnowledgeNo:{i+1}")

        knowledge_content=KnowledgeApiClient.fetch_knowledge_content(knowledge_no=str(i+1))

        if knowledge_content and knowledge_content['content']:

            
            parser = HtmlParser()

            
            md_content=parser.parse_html_to_markdown(str(i+1),knowledge_content)

            
            
            md_title=knowledge_content.get('title',"无标题")

            
            clean_title=TextUtils.clean_filename(md_title.strip())

            
            if len(clean_title)>50:
                clean_title=clean_title[:50].rstrip("_")

            

            file_name=f"{i+1:04d}-{clean_title}.md"

            
            file_path=os.path.join(settings.CRAWL_OUTPUT_DIR, file_name)

            
            FileRepository.save_file(md_content,file_path)
            success+=1
            print(f" {i+1}-> 保存成功:{file_name} ")

        else:
            fail+=1
            print(f" {i+1}-> 暂无内容,保存失败")


        time.sleep(0.05)

    print(f"\n爬取完成! 成功: {success}, 失败: {fail}")



if __name__ == '__main__':
    main()


















































