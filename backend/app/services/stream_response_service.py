from collections.abc import AsyncGenerator
from agents.run import RunResultStreaming
from openai.types.responses.response_stream_event import (
    ResponseTextDeltaEvent,
    ResponseReasoningTextDeltaEvent,
    ResponseReasoningSummaryTextDeltaEvent,
)
from agents.items import ToolCallItem

from utils.response_util import ResponseFactory
from utils.text_util import format_tool_call_html, format_agent_update_html
from schemas.response import ContentKind


async def process_stream_response(streaming_result: RunResultStreaming) -> AsyncGenerator:
    """
    处理Agent流式的事假
    Args:
        streaming_result:  流式结果对象（RunResultStreaming）
    Returns:

    """

    async for event in streaming_result.stream_events():
        
        
        
        if event.type == "raw_response_event":
            
            if isinstance(event.data, ResponseTextDeltaEvent):
                delta_text = event.data.delta
                yield "data: " + ResponseFactory.build_text(
                    delta_text, ContentKind.ANSWER
                ).model_dump_json() + "\n\n"

            
            elif ResponseReasoningTextDeltaEvent and isinstance(event.data, ResponseReasoningTextDeltaEvent):
                if event.data.delta:
                    yield "data: " + ResponseFactory.build_text(
                        event.data.delta, ContentKind.THINKING
                    ).model_dump_json() + "\n\n"

            
            elif isinstance(event.data, ResponseReasoningSummaryTextDeltaEvent):
                if event.data.delta:
                    yield "data: " + ResponseFactory.build_text(
                        event.data.delta, ContentKind.THINKING
                    ).model_dump_json() + "\n\n"

        
        
        
        elif event.type == "run_item_stream_event":
            if hasattr(event, "name") and event.name == "tool_called":
                if isinstance(event.item, ToolCallItem) and event.item.type == "tool_call_item":
                    tool_name = event.item.raw_item.name

                    text = format_tool_call_html(tool_name)
                    
                    yield "data: " + ResponseFactory.build_text(
                        text, ContentKind.PROCESS
                    ).model_dump_json() + "\n\n"

        
        
        
        elif event.type == "agent_updated_stream_event":
            new_agent_name = event.new_agent.name

            text = format_agent_update_html(new_agent_name)

            yield "data: " + ResponseFactory.build_text(
                text, ContentKind.PROCESS
            ).model_dump_json() + "\n\n"

        
        
        
    yield "data: " + ResponseFactory.build_finish().model_dump_json() + "\n\n"
