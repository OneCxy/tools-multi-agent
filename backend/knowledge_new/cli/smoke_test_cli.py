"""Live ingestion and query checks; run explicitly with python -m cli.smoke_test_cli."""

import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from config.settings import settings
from services.ingestion.ingestion_processor import IngestionProcessor
from services.retrieval_service import RetrievalService
from services.query_service import QueryService


def main():
    logging.getLogger().setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    report_path = Path(settings.MD_FOLDER_PATH).parent / 'cutting_tool_admin' / 'live_test_results.json'
    report = {'ingestion': {}, 'queries': []}

    def save():
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

    processor = IngestionProcessor()
    database = processor.vector_store.vector_database
    existing = database.get(include=['metadatas', 'documents'])
    known = {}
    for metadata, content in zip(existing['metadatas'], existing['documents']):
        if metadata and metadata.get('source'):
            known.setdefault(str(Path(metadata['source']).resolve()), []).append(content)
    paths = sorted(Path(settings.MD_FOLDER_PATH).glob('*.md'))
    pending = []
    for path in paths:
        content = path.read_text(encoding='utf-8')
        if len(content) >= 3000:
            raise RuntimeError('This resume check expects single-chunk cards.')
        old = known.get(str(path.resolve()), [])
        if old:
            if old != [content]:
                raise RuntimeError(f'Existing content differs or is duplicated: {path.name}')
        else:
            pending.append(path)
    report['ingestion'] = {'files': len(paths), 'before': len(existing['ids']), 'pending': len(pending), 'added_chunks': 0, 'failures': []}
    save()
    print(f'INGEST files={len(paths)} pending={len(pending)}', flush=True)
    started = time.monotonic()
    
    if pending:
        processor.vector_store.embedd_document('embedding connectivity check')
    with ThreadPoolExecutor(max_workers=1) as pool:
        futures = {pool.submit(processor.ingest_file, str(path.resolve())): path for path in pending}
        for index, future in enumerate(as_completed(futures), 1):
            path = futures[future]
            try:
                report['ingestion']['added_chunks'] += future.result()
            except Exception as exc:
                report['ingestion']['failures'].append({'file': path.name, 'error_type': type(exc).__name__})
            if index % 20 == 0 or index == len(pending):
                save()
                print(f'INGEST {index}/{len(pending)} failures={len(report["ingestion"]["failures"])} elapsed={time.monotonic()-started:.1f}s', flush=True)
    report['ingestion']['after'] = database._collection.count()
    report['ingestion']['seconds'] = round(time.monotonic() - started, 2)
    save()
    if report['ingestion']['failures']:
        raise RuntimeError('Ingestion failed; see report. Rerun resumes unchanged documents.')

    retrieval = RetrievalService()
    query = QueryService()
    cases = [
        ('iso', 'ISO刀片型号第二位的后角代码C是什么意思？', 'ISO刀片后角代码C'),
        ('formula', '车削时切削速度190 m/min，工件直径55 mm，转速如何计算？', '车削转速计算'),
        ('failure', '车削刀片出现随机崩刃，可能有哪些原因，应该如何检查？', '随机崩刃'),
        ('grade', 'Tungaloy T9205牌号的ISO应用范围是什么？能直接替代其他品牌吗？', 'T9205'),
        ('out_of_scope', '北京明天的天气和气温是多少？', None),
    ]
    for name, question, expected in cases:
        started = time.monotonic()
        result = {'case': name, 'question': question}
        try:
            docs = retrieval.retrieval(question)
            result['titles'] = [doc.metadata.get('title', '') for doc in docs]
            result['expected_title_hit'] = any(expected in title for title in result['titles']) if expected else None
            result['answer'] = query.generate_answer(question, docs)
            result['seconds'] = round(time.monotonic() - started, 2)
        except Exception as exc:
            result['error_type'] = type(exc).__name__
        report['queries'].append(result)
        save()
        print(json.dumps(result, ensure_ascii=False), flush=True)

    from fastapi.testclient import TestClient
    from api.main import create_fast_api
    with TestClient(create_fast_api()) as client:
        response = client.post('/query', json={'question': cases[0][1]})
        report['api'] = {'status_code': response.status_code, 'body': response.json()}
    save()
    print('API ' + json.dumps(report['api'], ensure_ascii=False), flush=True)
    print(f'REPORT {report_path}', flush=True)


if __name__ == '__main__':
    main()
