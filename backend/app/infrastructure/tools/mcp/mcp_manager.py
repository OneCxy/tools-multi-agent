from infrastructure.logging.logger import logger
from infrastructure.tools.mcp.mcp_servers import baidu_mcp_client


async def mcp_connect():
    """建立刀具供应商定位所需的百度地图 MCP 连接。"""
    await baidu_mcp_client.connect()
    logger.info("百度地图 MCP 连接建立完成")


async def mcp_cleanup():
    """清理百度地图 MCP 连接。"""
    await baidu_mcp_client.cleanup()
    logger.info("百度地图 MCP 连接已清理")
