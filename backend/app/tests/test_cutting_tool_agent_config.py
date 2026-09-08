from pathlib import Path
import unittest

from multi_agent.agent_factory import AGENT_TOOLS
from multi_agent.cutting_tool_agent import cutting_tool_agent
from multi_agent.sales_order_agent import sales_order_agent
from multi_agent.supplier_locator_agent import cutting_tool_supplier_agent


class CuttingToolAgentConfigTest(unittest.TestCase):
    def test_registered_agent_tools_match_business_boundaries(self):
        self.assertEqual(
            [tool.name for tool in AGENT_TOOLS],
            [
                "consult_cutting_tool_expert",
                "consult_sales_order_agent",
                "locate_cutting_tool_suppliers",
            ],
        )

    def test_agent_names_are_business_specific(self):
        self.assertEqual(cutting_tool_agent.name, "刀具技术咨询专家")
        self.assertEqual(sales_order_agent.name, "销售报价与订单协同专家")
        self.assertEqual(cutting_tool_supplier_agent.name, "刀具供应商定位专家")

    def test_active_orchestrator_prompt_contains_route_boundaries(self):
        prompt_path = Path(__file__).parents[1] / "prompts" / "orchestrator_v1.md"
        prompt = prompt_path.read_text(encoding="utf-8")
        self.assertIn("consult_cutting_tool_expert", prompt)
        self.assertIn("consult_sales_order_agent", prompt)
        self.assertIn("locate_cutting_tool_suppliers", prompt)
        self.assertIn("实时库存", prompt)
        self.assertIn("故障诊断", prompt)


if __name__ == "__main__":
    unittest.main()
