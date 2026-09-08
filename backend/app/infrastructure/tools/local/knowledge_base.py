import httpx
from agents import function_tool

from config.settings import settings
from infrastructure.logging.logger import logger


async def fetch_cutting_tool_knowledge(question: str) -> dict:
    """调用数控刀具知识库 HTTP 接口。"""
    if not settings.KNOWLEDGE_BASE_URL:
        return {"status": "error", "error_msg": "未配置知识库服务地址"}

    async with httpx.AsyncClient(trust_env=False) as client:
        try:
            response = await client.post(
                url=f"{settings.KNOWLEDGE_BASE_URL}/query",
                json={"question": question},
                timeout=120,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:
            logger.error(f"数控刀具知识库请求失败: {exc}")
            return {
                "status": "error",
                "error_msg": f"数控刀具知识库请求失败: {exc}",
            }
        except Exception as exc:
            logger.error(f"数控刀具知识库发生未知错误: {exc}")
            return {"status": "error", "error_msg": f"未知错误: {exc}"}


@function_tool
async def query_cutting_tool_knowledge(question: str) -> dict:
    """查询数控刀具知识库。

    适用于刀片型号解释、刀片与刀杆匹配、材料分类、刀具选型、
    切削参数、公式计算以及磨损和故障诊断。

    Args:
        question: 需要查询的完整刀具技术问题。

    Returns:
        包含 question、answer 和 sources 的知识库响应。
    """
    return await fetch_cutting_tool_knowledge(question)



query_knowledge = query_cutting_tool_knowledge
