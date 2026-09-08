import re
from collections.abc import AsyncGenerator
from agents.run import Runner, RunConfig
from multi_agent.orchestrator_agent import orchestrator_agent
from schemas.request import ChatMessageRequest
from services.session_service import session_service
from services.stream_response_service import process_stream_response
from utils.response_util import ResponseFactory
from infrastructure.logging.logger import logger
import traceback
from schemas.response import ContentKind


class MultiAgentService:
    """多智能体业务服务。"""

    @classmethod
    async def process_task(cls, request: ChatMessageRequest, flag: bool) -> AsyncGenerator:
        """
        多智能体处理任务入口
        Args:
            request:  请求上下文

        Returns:
            AsyncGenerator：异步生成器对象（必须）
        """
        try:
            
            user_id = request.context.user_id
            session_id = request.context.session_id
            user_query = request.query

            
            chat_history = session_service.prepare_history(user_id, session_id, user_query)

            
            streaming_result = Runner.run_streamed(
                starting_agent=orchestrator_agent,
                input=chat_history,  
                context=user_query,  
                max_turns=5,  
                run_config=RunConfig(tracing_disabled=True)
            )

            
            async for chunk in process_stream_response(streaming_result):
                yield chunk

            
            agent_result = streaming_result.final_output

            format_agent_result = re.sub(r'\n+', '\n', agent_result)
            
            chat_history.append({"role": "assistant", "content": format_agent_result})

            session_service.save_history(user_id, session_id, chat_history)
        except Exception as e:
            
            logger.error(f"AgentService.process_query执行出错: {str(e)}")
            logger.debug(f"异常详情: {traceback.format_exc()}")

            text = f"❌ 系统错误: {str(e)}"
            yield "data: " + ResponseFactory.build_text(
                text, ContentKind.PROCESS
            ).model_dump_json() + "\n\n"

            
            if flag:
                text = f"🔄 正在尝试自动重试..."
                yield "data: " + ResponseFactory.build_text(
                    text, ContentKind.PROCESS
                ).model_dump_json() + "\n\n"

                
                async for item in MultiAgentService.process_task(request,flag=False):
                    yield item
