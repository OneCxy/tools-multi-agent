# 数控刀具智能问询系统

基于多智能体与 RAG 的数控刀具问询系统，面向刀具选型、参数推荐、型号解释和加工故障诊断等场景。系统支持流式问答、知识库检索、历史会话、销售订单咨询及附近供应商查询。

项目：`tools-multi-agent`

## 主要功能

- 数控刀具型号、选型与兼容性咨询
- 切削参数计算与加工故障诊断
- Markdown 知识文档上传和 RAG 检索
- 多智能体任务识别与自动路由
- SSE 流式回答及工具调用过程展示
- 历史会话保存与恢复
- 销售订单咨询和附近供应商查询

## 技术栈

- 前端：Vue 3、Vite、Element Plus
- 后端：Python、FastAPI、OpenAI Agents SDK
- 知识库：LangChain、Chroma、Jieba、Embedding 模型
- 外部能力：OpenAI 兼容模型接口、百度地图 MCP

## 项目结构

```text
├─ backend/
│  ├─ app/                    # 多智能体后端
│  └─ knowledge_new/          # RAG 知识库后端
├─ front/
│  ├─ agent_web_ui/           # 主聊天前端
│  └─ knowledge_platform_ui/  # 知识库管理前端
└─ README.md                   # 项目说明
```

## 环境要求

- Python 3.11
- Node.js 18+
- npm 9+
- Conda（推荐）或 Python venv

## 安装依赖

建议为两个 Python 后端分别创建环境。

### 知识库后端

```bash
cd backend/knowledge_new
python -m pip install -r requirements.txt
python -m pip install -e .
```

### 多智能体后端

```bash
cd backend/app
python -m pip install -r requirements.txt
python -m pip install -e .
```

### 前端

```bash
cd front/agent_web_ui
npm install

cd ../knowledge_platform_ui
npm install
```

## 配置环境变量

```powershell
Copy-Item backend/knowledge_new/.env.example backend/knowledge_new/.env
Copy-Item backend/app/.env.example backend/app/.env
```


## 快速启动


### 1. 知识库后端

```bash
cd backend/knowledge_new
python -m api.main
```

- 接口地址：`http://127.0.0.1:8001`
- 接口文档：`http://127.0.0.1:8001/docs`

### 2. 多智能体后端

```bash
cd backend/app
python -m api.main
```

- 接口地址：`http://127.0.0.1:8000`
- 接口文档：`http://127.0.0.1:8000/docs`

### 3. 主聊天前端

```bash
cd front/agent_web_ui
npm run dev
```

访问：`http://localhost:5173`

### 4. 知识库管理前端（可选）

```bash
cd front/knowledge_platform_ui
npm run dev
```

访问：`http://localhost:3000`

## 初始化知识库


```bash
cd backend/knowledge_new
python -m cli.upload_cli
```

知识文档默认位于 `backend/knowledge_new/data/cutting_tool/`
