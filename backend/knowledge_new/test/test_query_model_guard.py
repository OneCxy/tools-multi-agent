import unittest

from langchain_core.documents import Document

from services.query_service import QueryService


class QueryModelGuardTest(unittest.TestCase):
    def test_rejects_model_code_missing_from_context(self):
        documents = [Document(page_content="ISO P钢精车需要确认硬度。", metadata={"title": "ISO P钢精车"})]
        self.assertEqual(
            QueryService.find_unsupported_model_codes("CNMG120408适合45钢精车吗？", documents),
            ["CNMG120408"],
        )

    def test_accepts_model_code_present_in_context(self):
        documents = [Document(page_content="T9205适用于指定材料范围。", metadata={"title": "T9205材质"})]
        self.assertEqual(
            QueryService.find_unsupported_model_codes("T9205适合什么材料？", documents),
            [],
        )


if __name__ == "__main__":
    unittest.main()
