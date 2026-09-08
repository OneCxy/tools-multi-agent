from agents import Agent, ModelSettings

from infrastructure.ai.openai_client import sub_model
from infrastructure.ai.prompt_loader import load_prompt


sales_order_agent = Agent(
    name="销售报价与订单协同专家",
    instructions=load_prompt("sales_order_agent"),
    model=sub_model,
    model_settings=ModelSettings(temperature=0),
    tools=[],
)
