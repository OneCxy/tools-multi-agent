from agents import Agent, ModelSettings

from infrastructure.ai.openai_client import sub_model
from infrastructure.ai.prompt_loader import load_prompt
from infrastructure.tools.local.knowledge_base import query_cutting_tool_knowledge


cutting_tool_agent = Agent(
    name="刀具技术咨询专家",
    instructions=load_prompt("cutting_tool_agent"),
    model=sub_model,
    model_settings=ModelSettings(temperature=0),
    tools=[query_cutting_tool_knowledge],
)
