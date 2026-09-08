import  os
import re
from typing import List,Dict,Any


class MarkDownUtils:
    """
     MarkDown文档处理工具
    """

    @staticmethod
    def collect_md_metadata(folder_path: str) -> List[Dict[str, Any]]:
        """
        收集Markdown文件元数据

        遍历指定目录，提取所有Markdown文件的路径和标题信息。

        Args:
            folder_path: Markdown文件所在目录

        Returns:
            List[Dict[str, Any]]: 包含路径和标题的元数据列表
        """
        md_metadata = []
        if not os.path.exists(folder_path):
            return md_metadata

        
        filename_pattern = re.compile(r'^(.+?)-(.*?)\.md$')

        for filename in os.listdir(folder_path):
            if filename.endswith('.md'):
                match = filename_pattern.match(filename)
                if match:
                    title = match.group(2).strip()
                else:
                    title = os.path.splitext(filename)[0].strip()

                md_metadata.append({
                    "path": os.path.join(folder_path, filename),
                    "title": title
                })
        return md_metadata

    @staticmethod
    def extract_title(file_path: str) -> str:
        """
        辅助方法：从文件名中提取标题
        逻辑与 MarkDownUtils 保持一致
        """
        filename = os.path.basename(file_path)
        filename_pattern = re.compile(r'^(.+?)-(.*?)\.md$')
        match = filename_pattern.match(filename)
        if match:
            
            return match.group(2).strip()
        else:
            
            return os.path.splitext(filename)[0].strip()

    def clean_markdown_images(text: str) -> str:
        """将 ![描述](url) 替换为纯 url，每张图单独一行"""
        
        pattern = r'!\$$[^$$]*\]\((https?://[^\s\)]+)\)'

        def replace_func(match):
            url = match.group(1)
            return f"\n{url}\n"  

        cleaned = re.sub(pattern, replace_func, text)

        
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

        return cleaned.strip()

