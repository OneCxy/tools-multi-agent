"""
应用配置管理模块

使用 pydantic-settings 进行配置管理，支持：
1. 自动从环境变量读取配置
2. 类型验证和转换
3. 默认值设置
4. 配置文档化
"""
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from typing_extensions import Self


class Settings(BaseSettings):
    """
    应用配置类

    配置项会自动从以下来源读取（优先级从高到低）：
    1. 环境变量
    2. .env 文件
    3. 默认值
    """

    

    
    SF_API_KEY: Optional[str] = Field(default=None, description="硅基流动 API Key")
    SF_BASE_URL: Optional[str] = Field(default=None, description="硅基流动 Base URL")

    
    AL_BAILIAN_API_KEY: Optional[str] = Field(default=None, description="阿里百炼 API Key")
    AL_BAILIAN_BASE_URL: Optional[str] = Field(default=None, description="阿里百炼 Base URL")

    

    MAIN_MODEL_NAME: Optional[str] = Field(
        default="Qwen/Qwen3-32B",
        description="主模型名称"
    )
    SUB_MODEL_NAME: Optional[str] = Field(
        default="",
        description="qwen3-max"
    )

    

    
    KNOWLEDGE_BASE_URL: Optional[str] = Field(
        default=None,
        description="知识库服务URL"
    )

    
    DASHSCOPE_BASE_URL: Optional[str] = Field(
        default=None,
        description="通义千问 DashScope Base URL"
    )
    DASHSCOPE_API_KEY: Optional[str] = Field(
        default=None,
        description="通义千问 DashScope API Key"
    )

    
    BAIDUMAP_AK: Optional[str] = Field(
        default=None,
        description="百度地图 AK (Access Key)"
    )

    

    model_config = SettingsConfigDict(
        
        env_file=str(Path(__file__).parent.parent / ".env"),
        env_file_encoding="utf-8",          
        case_sensitive=True,                 
        extra="ignore",                      
        validate_default=True,               
    )

    
    @model_validator(mode='after')
    def check_ai_service_configuration(self) -> Self:
        """
        验证器：在配置加载完成后自动执行。
        如果需要强制至少配置一个 AI 服务，可以在这里抛出 ValueError
        """
        
        has_service = any([
            self.SF_API_KEY and self.SF_BASE_URL,
            self.AL_BAILIAN_API_KEY and self.AL_BAILIAN_BASE_URL
        ])

        if not has_service:
            raise ValueError("必须配置至少一个 AI 服务 (硅基流动 或 阿里百炼)")

        return self




settings = Settings()

