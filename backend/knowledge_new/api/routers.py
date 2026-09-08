import os.path
import logging
import aiofiles
import shutil

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool
from services.ingestion.ingestion_processor import IngestionProcessor
from schemas.schema import QueryRequest, QueryResponse, SourceReference, UploadResponse
from services.retrieval_service import RetrievalService
from services.query_service import QueryService
from config.settings import settings

import tempfile


router = APIRouter()

ingestion_processor = IngestionProcessor()
retrieval_service = RetrievalService()
query_service = QueryService()



@router.post("/upload", response_model=UploadResponse, summary="处理知识库上传")
async def upload_file(file: UploadFile = File(...)):
    

    temp_file_path = None
    try:
        
        temp_md_dir = settings.TMP_MD_FOLDER_PATH
        file_suffix = os.path.splitext(file.filename)[1]
        tmp_md_path = os.path.join(temp_md_dir, file.filename)
        if not os.path.exists(tmp_md_path):
            os.makedirs(temp_md_dir, exist_ok=True)

        
        async with aiofiles.tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as temp_file:

            
            while content := await file.read(1024 * 1024):
                
                await temp_file.write(content)

            
            temp_file_path = temp_file.name

        shutil.move(temp_file_path, tmp_md_path)

        
        chunks_added = await run_in_threadpool(ingestion_processor.ingest_file, tmp_md_path)
        print(f"临时文件路径:{temp_file_path}")

        
        return UploadResponse(
            status="success",
            message="文档上传知识库成功",
            file_name=file.filename,
            chunks_added=chunks_added
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"文件上传到知识库失败:{str(e)}")

    finally:
        
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.info(f"临时文件:{temp_file_path}已删除...")


@router.post("/query", response_model=QueryResponse, summary="查询知识库")
async def query(request: QueryRequest):
    """
    查询知识库
    Args:
        request: 用户的输入请求

    Returns:
        QueryResponse： 模型的结果以及原始问题

    """
    try:
        
        user_question = request.question
        if not user_question:
            raise HTTPException(status_code=500, detail="查询问题不存在")

        
        retrieval_context = await run_in_threadpool(
            retrieval_service.retrieval,
            user_question,
        )

        
        answer = await run_in_threadpool(
            query_service.generate_answer,
            user_question,
            retrieval_context,
        )

        
        unsupported_codes = query_service.find_unsupported_model_codes(
            user_question,
            retrieval_context,
        )
        sources = []
        seen_sources = set()
        for document in [] if unsupported_codes else retrieval_context:
            source_path = document.metadata.get("source") or document.metadata.get("path", "")
            title = document.metadata.get("title") or os.path.splitext(os.path.basename(source_path))[0]
            file_name = os.path.basename(source_path)
            source_key = (title, file_name)
            if source_key not in seen_sources:
                seen_sources.add(source_key)
                sources.append(SourceReference(title=title, file_name=file_name))

        return QueryResponse(
            question=user_question,
            answer=answer,
            sources=sources,
        )
    except Exception as e:
        logger.error(f"调用查询知识库服务失败:原因:{str(e)}")
        raise HTTPException(status_code=500,detail="服务内部出现异常")
