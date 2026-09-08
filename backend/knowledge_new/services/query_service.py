import re
from typing import List
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from config.settings import settings

class QueryService:
    """检索服务"""

    def __init__(self):

        self.llm=ChatOpenAI(model_name=settings.MODEL,
                            openai_api_key=settings.API_KEY,
                            openai_api_base=settings.BASE_URL,
                            temperature=0) 



    def generate_answer(self, user_question:str, retrival_context: List[Document]) -> str:
        """
        对接大语言模型的入口
        Args:
            user_question: 用户问题
            retrival_context: 检索到的上下文

        Returns:
            str:LLM模型整合上下文之后的自然语言
        """

        
        if not  retrival_context:
            return "未检索到任何相关的文档，无法提供回复"

        unsupported_codes = self.find_unsupported_model_codes(user_question, retrival_context)
        if unsupported_codes:
            codes = "、".join(unsupported_codes)
            return (
                f"当前检索资料未包含型号 {codes} 的完整定义、厂商牌号和适用范围，"
                "因此无法确认型号含义、兼容性或选型结果。请补充厂商名称、完整型号及材质牌号；"
                "如需判断加工适用性，还需提供工件材料硬度、加工工序、连续或断续切削、"
                "机床稳定性和表面质量要求。"
            )


        
        context_blocks = []
        for index, document in enumerate(retrival_context):
            title = document.metadata.get("title", "未命名资料")
            context_blocks.append(
                f"资料{index + 1}\n标题：{title}\n内容：\n{document.page_content}"
            )
        retrival_context = "\n\n".join(context_blocks)

        
        prompt = f"""
        你是一位数控刀具技术顾问。请严格基于下方的【参考资料】回答【用户问题】。

         【参考资料】：
         ```
         {retrival_context}
         ```

         【用户问题】：
         ```
         {user_question}
         ```

         【回答要求】：
         1. 严格依据参考资料，不编造刀片牌号、适用范围、兼容关系或切削参数。
         2. 型号解释应逐位说明字符含义；资料不足时明确指出无法确认的部分。
         3. 选型前检查材料、硬度、工序、粗精加工、连续或断续切削、机床稳定性和表面质量要求。必要条件缺失时先列出需要补充的信息。
         4. 参数必须包含符号、数值、单位、适用条件，并说明属于初始建议，需要结合具体牌号、机床和工况试切调整。
         5. 故障诊断按“可能原因、检查方法、处理措施”组织。涉及刀片松动、刀体损伤、撞击或连续崩刃时，应建议停机检查。
         6. 不处理价格、实时库存、交期、订单、物流和客户信用问题。
         7. 如果资料无法回答，直接回答：“当前的知识库中暂时没有找到该问题的解决方案。”
         8. 语言简洁、专业、直接；回答末尾列出实际采用的资料编号和标题。
         9. 每一项结论都必须得到参考资料的直接支持。不得把不相关资料中的品牌、牌号、材料组或应用区间套用到用户对象上。
         10. 型号、材料或工况不一致的资料只能视为不相关资料，不得用于推断。例如，不得把材料名称中的数字“45”理解为ISO应用区间中的“M45”。
         11. 如果参考资料只说明通用核对方法，回答只能列出核对方法和缺失字段，不得补充参考资料中其他产品的具体参数。

         【开始回答】：
         """

        
        llm_response=self.llm.invoke(prompt)


        
        return  llm_response.content

    @staticmethod
    def find_unsupported_model_codes(
        user_question: str,
        retrieval_context: List[Document],
    ) -> List[str]:
        """找出问题中未被召回资料直接覆盖的英文数字型号。"""
        model_codes = re.findall(
            r"(?<![A-Za-z0-9])(?=[A-Z0-9-]{4,})(?=[A-Z0-9-]*[A-Z])(?=[A-Z0-9-]*\d)[A-Z0-9-]+",
            user_question,
        )
        if not model_codes:
            return []

        context_text = "\n".join(
            f"{document.metadata.get('title', '')}\n{document.page_content}"
            for document in retrieval_context
        ).upper()
        return [code for code in dict.fromkeys(model_codes) if code.upper() not in context_text]





