from pydantic_settings import BaseSettings,SettingsConfigDict
import os

class Settings(BaseSettings):
    API_KEY: str = os.environ.get("API_KEY")
    BASE_URL: str = os.environ.get("BASE_URL")
    MODEL: str = os.environ.get("MODEL")
    EMBEDDING_API_KEY: str = os.environ.get("EMBEDDING_API_KEY")
    EMBEDDING_BASE_URL: str = os.environ.get("EMBEDDING_BASE_URL")
    EMBEDDING_MODEL: str = os.environ.get("EMBEDDING_MODEL")

    
    
    KNOWLEDGE_BASE_URL:str=os.environ.get("KNOWLEDGE_BASE_URL")

    _current_dir = os.path.dirname(os.path.abspath(__file__))
    
    _project_root = os.path.dirname(_current_dir)
    
    VECTOR_STORE_PATH: str = os.path.join(_project_root, "chroma_cnc_tools")
    
    
    CRAWL_OUTPUT_DIR: str = os.path.join(_project_root, "data", "crawl")
    
    MD_FOLDER_PATH: str = os.path.join(_project_root, "data", "cutting_tool")
    TMP_MD_FOLDER_PATH:str= os.path.join(_project_root, "data", "tmp")
    
    CHUNK_SIZE: int = 3000
    CHUNK_OVERLAP: int = 200

    
    TOP_ROUGH: int = 50
    TOP_FINAL: int = 5
    VECTOR_DISTANCE_THRESHOLD: float = 0.8
    TITLE_ROUGH_SCORE_THRESHOLD: float = 0.08

    model_config = SettingsConfigDict(
        env_file=os.path.join(_project_root, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
