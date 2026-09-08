from typing import Dict, Any
from  utils.text_utils import TextUtils


class HtmlParser:
    """专门负责解析Html格式数据成为MarkDown格式的数据"""

    def parse_html_to_markdown(self, knowledge_no: str, html_data: Dict[str, Any]) -> str:
        """
        解析html格式成为markdown格式
        :param html_data:html格式数据
        :return:markdown格式的字符串数据
        """

        
        if  not html_data['content']:
            raise ValueError("要解析的数据不存在")

        
        
        items = [f"# 知识库 {knowledge_no}\n"]  

        
        html_data_title = html_data.get('title', '暂无标题')
        items.append(f"## 标题\n{html_data_title.strip()}\n")

        
        html_data_digest= html_data['digest']
        if html_data_digest and html_data_digest.strip():
            items.append(f"## 问题描述\n{html_data_digest.strip()}\n")

        
        
        first_topic_name = html_data['firstTopicName']
        sub_topic_name = html_data['subTopicName']
        question_category_name = html_data['questionCategoryName']

        categories=[]
        if  first_topic_name and first_topic_name.strip():
            categories.append(f"主类别: {first_topic_name.strip()}")
        if  sub_topic_name and sub_topic_name.strip():
            categories.append(f"子类别: {sub_topic_name.strip()}")
        elif question_category_name and question_category_name.strip():
            categories.append(f"问题类别: {question_category_name}")

        if  categories:
            items.append(f"## 分类\n"+"\n".join(categories)+"\n")

        
        html_data_key_words=html_data['keyWords']
        key_words_list=[]
        if html_data_key_words:
            for key_world in  html_data_key_words:
                if isinstance(key_world,str):
                   
                   key_words_list.extend([key_world.strip() for key_world in  key_world.split(",") if key_world.strip()])
            if key_words_list:
                keywords = ", ".join(key_words_list)
                items.append(f"## 关键词\n{keywords}\n")


        
        medata_data = []
        html_data_create_time=html_data['createTime']
        html_data_version_no=html_data['versionNo']
        if html_data_create_time and html_data_create_time.strip():
            medata_data.append(f"创建时间:{html_data_create_time.strip()}")
        if html_data_version_no and html_data_version_no.strip():
            medata_data.append(f"版本:{html_data_version_no.strip()}")
        if medata_data:
            items.append(f"## 元信息\n" + "|".join(medata_data) + "\n")

        
        html_data_content=html_data['content']
        if  html_data_content:

            
            
            md_content=TextUtils.html_to_markdown(html_data_content)

            items.append(f"## 解决方案\n{md_content}\n")


        
        items.append(f"<!-- 文档主题：{html_data_title} (知识库库编号: {knowledge_no}) -->")

        return  "\n".join(items)


























