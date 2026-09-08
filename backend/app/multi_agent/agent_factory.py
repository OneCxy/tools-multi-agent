from agents import Runner, function_tool
from agents.run import RunConfig

from infrastructure.logging.logger import logger
from infrastructure.tools.local.knowledge_base import fetch_cutting_tool_knowledge
from multi_agent.sales_order_agent import sales_order_agent
from multi_agent.supplier_locator_agent import cutting_tool_supplier_agent


@function_tool
async def consult_cutting_tool_expert(query: str) -> str:
    """处理数控刀具技术问题。

    适用于刀片或刀杆型号解释、刀具兼容性、选型、切削参数计算与
    初始建议，以及崩刃、磨损、振纹、毛刺和切屑控制等故障诊断。

    Args:
        query: 用户当前消息中的完整刀具技术问题及已知工况。
    """
    try:
        logger.info(f"[Route] 转交刀具技术咨询专家: {query[:30]}...")
        result = await fetch_cutting_tool_knowledge(query)
        if result.get("status") == "error":
            return result["error_msg"]

        answer = result.get("answer", "当前的知识库中暂时没有找到该问题的解决方案。").strip()
        sources = result.get("sources", [])
        source_files = [source.get("file_name") for source in sources if source.get("file_name")]
        if source_files:
            answer += "\n\n来源文件：" + "、".join(source_files)
        return answer
    except Exception as exc:
        logger.error(f"刀具技术咨询专家执行失败: {exc}")
        return f"刀具技术咨询暂时无法完成: {exc}"


@function_tool
async def consult_sales_order_agent(query: str) -> str:
    """处理刀具销售报价与订单业务。

    适用于价格、实时库存、报价、交期、订单修改或状态、物流状态和
    客户信用等请求。当前未接入实时业务数据库时，只收集必要信息，
    不得编造业务结果。

    Args:
        query: 用户当前消息中的销售或订单请求及已提供字段。
    """
    try:
        logger.info(f"[Route] 转交销售报价与订单协同专家: {query[:30]}...")
        result = await Runner.run(
            sales_order_agent,
            input=query,
            run_config=RunConfig(tracing_disabled=True),
        )
        return result.final_output
    except Exception as exc:
        logger.error(f"销售报价与订单协同专家执行失败: {exc}")
        return f"销售报价与订单协同暂时无法完成: {exc}"


@function_tool
async def locate_cutting_tool_suppliers(query: str) -> str:
    """查找用户附近可能销售金属切削刀具的企业并提供导航。

    适用于“附近哪里购买数控刀具”“查找某品牌刀具经销商”和前往
    刀具供应商的导航请求，不用于查询实时库存、价格或技术选型。

    Args:
        query: 用户的位置、品牌及供应商查找要求。
    """
    try:
        logger.info(f"[Route] 转交刀具供应商定位专家: {query[:30]}...")
        result = await Runner.run(
            cutting_tool_supplier_agent,
            input=query,
            run_config=RunConfig(tracing_disabled=True),
        )
        return result.final_output
    except Exception as exc:
        logger.error(f"刀具供应商定位专家执行失败: {exc}")
        return f"刀具供应商定位暂时无法完成: {exc}"


AGENT_TOOLS = [
    consult_cutting_tool_expert,
    consult_sales_order_agent,
    locate_cutting_tool_suppliers,
]
