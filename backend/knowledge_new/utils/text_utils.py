from bs4 import BeautifulSoup,Tag
from markdownify import markdownify as md
import re


class TextUtils:
    @staticmethod
    def html_to_markdown(html_content: str) -> str:
        """
        HTML转Markdown (包含必要的 DOM 清洗)
        """
        if not html_content:
            return ""

        
        soup = BeautifulSoup(html_content, 'html.parser')

        
        
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose() 

        
        for ad in soup.select('.mceNonEditable'):
            ad.decompose() 

        
        

        
        bold_tags = soup.find_all(['strong', 'b'])
        for tag in bold_tags:
            
            if not tag.parent:
                continue
            
            next_sibling = tag.next_sibling

            
            
            
            
            if next_sibling and isinstance(next_sibling, Tag) and next_sibling.name == tag.name:
                
                
                tag.extend(next_sibling.contents)
                
                next_sibling.decompose()

        
        cleaned_html = str(soup)

        
        markdown_text = md(cleaned_html)
        return markdown_text

    @staticmethod
    def clean_filename(filename: str) -> str:
        """清洗文件名中的非法字符"""
        if not filename:
            return "untitled"
        illegal_chars = r'[\\/:*?"<>|]'
        return re.sub(illegal_chars, '-', filename)