import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.routers import router
from infrastructure.logging.logger import logger
from infrastructure.tools.mcp.mcp_manager import mcp_connect, mcp_cleanup


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI应用生命周期管理

    在应用启动时建立MCP连接，在应用关闭时清理连接。
    确保资源正确初始化和释放。
    """
    
    logger.info("应用启动，建立MCP连接...")
    try:
        await mcp_connect()
        logger.info("MCP连接建立完成")
    except Exception as e:
        logger.error(f"MCP连接建立失败: {str(e)}")

    yield  

    
    logger.info("应用关闭，清理MCP连接...")
    try:
        await mcp_cleanup()
        logger.info("MCP连接清理完成")
    except Exception as e:
        logger.error(f"MCP连接清理失败: {str(e)}")


def create_fast_api() -> FastAPI:
    
    app = FastAPI(title="Tools Multi-Agent API", lifespan=lifespan)

    
    app.add_middleware(
        CORSMiddleware,
        
        allow_origins=["*"],  
        allow_credentials=True,  
        allow_methods=["*"],  
        allow_headers=["*"],  
    )

    
    app.include_router(router=router)

    
    return app


if __name__ == '__main__':
    print("1.准备启动Web服务器")
    try:
        uvicorn.run(app=create_fast_api(), host="127.0.0.1", port=8000)

        logger.info("2.启动Web服务器成功...")

    except KeyboardInterrupt as e:
        logger.error(f"2.启动Web服务器失败: {str(e)}")
