# 刀具知识库资料管理

- 入库目录：`../cutting_tool/`，仅包含660份平铺的UTF-8 Markdown知识卡。
- 原始资料：`../cutting_tool_original/`，完整保留700份分类知识卡及原README、清单。
- 48篇公式示例合并为8篇，每篇保留一个明确变量、单位和结果的示例。
- 文件名使用`CTK编号-标题.md`，正文一级标题与文件名标题一致。
- `manifest.jsonl`记录整理后的标题、分类、路径和SHA-256；路径相对于`data/`。
- `migration_map.jsonl`记录700条原始记录与660份输出文件的对应关系；输出路径相对于`cutting_tool/`。
- 本次整理不代表全部技术结论已通过专业审核；非公式卡的技术正文保持原样。

## 运行

在`backend/knowledge_new`目录及知识库Python环境中执行：

```powershell
python -m cli.upload_cli
python -m api.main
```

入库和检索读取`settings.MD_FOLDER_PATH`；爬虫仍输出到独立的`data/crawl`。
整理过程未调用嵌入接口，未写入或清空向量库。重复执行现有入库命令可能重复添加向量。
