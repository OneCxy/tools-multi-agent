from agents import Agent, ModelSettings, set_tracing_disabled

from infrastructure.ai.openai_client import sub_model
from infrastructure.ai.prompt_loader import load_prompt
from infrastructure.tools.local.location_resolver import resolve_user_location_from_text
from infrastructure.tools.mcp.mcp_servers import baidu_mcp_client


set_tracing_disabled(True)


cutting_tool_supplier_agent = Agent(
    name="刀具供应商定位专家",
    instructions=load_prompt("supplier_locator_agent"),
    model=sub_model,
    model_settings=ModelSettings(temperature=0, max_tokens=2048),
    tools=[resolve_user_location_from_text],
    mcp_servers=[baidu_mcp_client],
)
