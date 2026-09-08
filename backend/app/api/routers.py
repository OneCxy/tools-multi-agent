from fastapi.routing import APIRouter
from starlette.responses import StreamingResponse

from schemas.request import ChatMessageRequest, UserSessionsRequest
from services.agent_service import MultiAgentService
from infrastructure.logging.logger import logger
from services.session_service import session_service


router = APIRouter()



@router.post("/api/query", summary="智能体对话接口")
async def query(request_context: ChatMessageRequest) -> StreamingResponse:
    """
    SSE返回数据（流式响应）
    响应头中：text/event-stream
    Args:
        request_context: 请求上下文

    Returns:
        StreamingResponse

    """

    
    user_id = request_context.context.user_id
    user_query = request_context.query
    print(request_context.flag)
    logger.info(f"用户 {user_id} 发送的待处理任务 {user_query}")

    
    async_generator_result = MultiAgentService.process_task(request_context, flag=True)

    
    return StreamingResponse(
        content=async_generator_result,
        status_code=200,
        media_type="text/event-stream"
    )


@router.post("/api/user_sessions")
def get_user_sessions(request: UserSessionsRequest):
    """
    获取用户的所有会话记忆数据。

    Args:
        request: 包含 user_id 的请求体。

    Returns:
        包含用户所有会话信息和记忆的 JSON 响应。
    """
    
    logger.info("接收到获取用户会话请求")

    
    user_id = request.user_id
    logger.info(f"获取用户 {user_id} 的所有会话记忆数据")

    try:
        
        all_sessions =session_service.get_all_sessions_memory(user_id)
        logger.debug(f"成功获取用户 {user_id} 的 {len(all_sessions)} 个会话")

        
        return {
            "success": True,
            "user_id": user_id,
            "total_sessions": len(all_sessions),
            "sessions": all_sessions
        }
    except Exception as e:
        
        logger.error(f"获取用户 {user_id} 的会话数据时出错: {str(e)}")
        return {
            "success": False,
            "user_id": user_id,
            "error": str(e)
        }
