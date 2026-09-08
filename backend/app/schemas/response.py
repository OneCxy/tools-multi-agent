from enum import Enum
from typing import Optional, Union, List, Literal
from pydantic import BaseModel, Field


class ContentKind(str, Enum):
    """
    内容语义分类：用于前端区分 UI 渲染逻辑。
    """
    THINKING = 'THINKING'  
    PROCESS = 'PROCESS'    
    ANSWER = 'ANSWER'      


class StreamStatus(str, Enum):
    """
    流状态：控制 SSE 连接的生命周期。
    """
    IN_PROGRESS = 'IN_PROGRESS'  
    FINISHED = 'FINISHED'        


class StopReason(str, Enum):
    """
    结束原因：仅当状态为 FINISHED 时有效。
    """
    NORMAL = 'NORMAL'          
    MAX_TOKENS = 'MAX_TOKENS'  
    ERROR = 'ERROR'            




class MessageBody(BaseModel):
    """消息体基类"""
    contentType: str


class TextMessageBody(MessageBody):
    """
    文本消息体：承载具体的流式内容。
    """
    contentType: Literal['sagegpt/text'] = 'sagegpt/text'
    text: str = Field(default='', description="实际文本内容")
    kind: ContentKind = Field(..., description="内容分类：THINKING/PROCESS/ANSWER")


class FinishMessageBody(MessageBody):
    """
    结束信号体：不包含内容，仅作为结束标志。
    """
    contentType: Literal['sagegpt/finish'] = 'sagegpt/finish'




class PacketMeta(BaseModel):
    """数据包元数据"""
    createTime: str
    finishReason: Optional[StopReason] = None
    errorMessage: Optional[str] = None


class StreamPacket(BaseModel):
    """
    SSE 流数据包 (原 MessageResponse)。
    这是后端 yield 给前端的最小数据单元。
    """
    id: str
    content: Union[TextMessageBody, FinishMessageBody]
    status: StreamStatus
    metadata: PacketMeta