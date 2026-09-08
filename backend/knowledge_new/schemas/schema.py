from typing import List

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """
     文件上传的响应数据模型
    """
    status:str  
    message:str 
    file_name:str 
    chunks_added:int 



class SourceReference(BaseModel):
    title: str
    file_name: str


class QueryResponse(BaseModel):
    """
     查询的响应数据模型
    """
    question:str 
    answer:str 
    sources: List[SourceReference] = Field(default_factory=list)

class QueryRequest(BaseModel):
    """
    查询的请求数据模型
    """
    question: str  

