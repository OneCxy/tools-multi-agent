"""Run live route checks with: python -m tests.live_cutting_tool_routes."""

import asyncio
import json
import sys

from agents import Runner, ToolCallItem

from multi_agent.orchestrator_agent import orchestrator_agent


CASES = [
    ("technical", "ISO刀片后角代码C是什么意思？"),
    ("sales", "CNMG120408现在有20片库存吗，多少钱？"),
    ("mixed", "CNMG120408适合45钢精车吗？现在有20片库存吗？"),
    ("out_of_scope", "北京明天天气怎么样？"),
]


async def main():
    selected_case = sys.argv[1] if len(sys.argv) > 1 else None
    for case_name, question in CASES:
        if selected_case and case_name != selected_case:
            continue
        result = await Runner.run(orchestrator_agent, input=question)
        tool_calls = []
        for item in result.new_items:
            if isinstance(item, ToolCallItem):
                tool_calls.append(item.raw_item.name)
        print(json.dumps({
            "case": case_name,
            "question": question,
            "tool_calls": tool_calls,
            "answer": result.final_output,
        }, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
