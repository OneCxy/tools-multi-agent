from pydantic import Field
from typing import  Optional
from pydantic import BaseModel

class UserContext(BaseModel):
    """
    用户上下文信息，用于标识请求来源。
    """
    user_id: str                                                          
    session_id: Optional[str] = Field(description="会话ID", default=None)  


class ChatMessageRequest(BaseModel):
    """
    用户发起聊天请求的入参结构。
    """
    query: str           
    context: UserContext 
    flag: bool = True    


class UserSessionsRequest(BaseModel):
    """
    获取用户历史会话列表的请求体。
    """
    user_id: str = Field(description="用户唯一标识符")     

