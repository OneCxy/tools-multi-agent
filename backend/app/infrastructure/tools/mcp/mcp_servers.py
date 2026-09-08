import asyncio
import json
from config.settings import settings
from agents.mcp import MCPServer, MCPServerSse, MCPServerStreamableHttp
from typing import Dict, Any


search_mcp_client = MCPServerStreamableHttp(
    name="通用联网搜索",
    params={
        "url": f"{settings.DASHSCOPE_BASE_URL}",
        "headers": {
            "Authorization": f"Bearer {settings.DASHSCOPE_API_KEY}"
        },
        "timeout": 60,  
        "sse_read_timeout": 60 * 30  
    },
    client_session_timeout_seconds=60 * 10,  
    cache_tools_list=True,
)


baidu_mcp_client = MCPServerSse(
    name="百度地图",
    params={  
        "url": f"https://mcp.map.baidu.com/sse?ak={settings.BAIDUMAP_AK}",
        "timeout": 60,  
        "sse_read_timeout": 60 * 30  
    },
    client_session_timeout_seconds=60 * 10,  
    cache_tools_list=True,
)





async def run_mcp_call(
        mcp_instance: MCPServer,
        tool_name: str,
        tool_args: Dict[str, Any]
):
    """
    执行流程：连接 -> 列出所有工具(看参数) -> 调用指定工具 -> 打印结果 -> 断开
    """
    server_name = mcp_instance.name
    print(f"\n{'=' * 60}")
    print(f" [测试启动] 服务: {server_name}")
    print(f"{'=' * 60}")

    try:
        
        print(f" [连接] 正在连接服务器...")
        await mcp_instance.connect()
        print(f" [连接] 成功")

        
        print(f"\n [列表] 正在获取工具列表及参数定义...")
        tools_list = await mcp_instance.list_tools()

        if tools_list:
            print(f"   发现 {len(tools_list)} 个工具：")
            for i, tool in enumerate(tools_list, 1):
                print(f"\n    [{i}] 工具名: {tool.name}")
                print(f"       描述: {tool.description}")
                print(f"       参数定义 (Schema):")
                
                print(json.dumps(tool.inputSchema, indent=2, ensure_ascii=False))
        else:
            print("    未获取到工具列表")

        print(f"\n{'-' * 40}")

        

        print(f"    发送参数: {json.dumps(tool_args, ensure_ascii=False)}")

        
        result = await mcp_instance.call_tool(tool_name, tool_args)
        print(f"\n [响应] 服务器返回结果:")

        
        for content in result.content:
            if hasattr(content, 'text'):
                
                
                
                json_res = content.text
                print(json_res)
            else:
                print(f" [Non-Text]: {content}")

    except Exception as e:
        print(f"\n [异常] 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        
        print(f"\n [断开] 正在清理连接...")
        await mcp_instance.cleanup()
        print(f" {server_name} 测试结束\n")






async def test_bailian_search():
    """
    测试百炼搜索 (使用全局 search_mcp)
    """
    await run_mcp_call(
        mcp_instance=search_mac_client,
        tool_name="bailian_web_search",  
        tool_args={"query": "数控刀具行业动态"}  
    )


async def test_baidu_map():
    """
    测试百度地图 (使用全局 baidu_mcp)
    """
    
    
    
    
    
    
    

    
    
    
    
    
    
    

    await run_mcp_call(
        mcp_instance=baidu_map_mcp,
        tool_name="map_uri",  
        tool_args={
            "service": "direction"
        }
    )



async def main():
    

    
    

    
    await test_baidu_map()


if __name__ == '__main__':
    asyncio.run(main())
