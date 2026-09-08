from agents import Agent, ModelSettings

from infrastructure.ai.openai_client import sub_model
from infrastructure.ai.prompt_loader import load_prompt
from multi_agent.agent_factory import AGENT_TOOLS


orchestrator_agent = Agent(
    name="数控刀具咨询主调度",
    instructions=load_prompt("orchestrator_v1"),
    model=sub_model,
    model_settings=ModelSettings(temperature=0),
    tools=AGENT_TOOLS,
)
