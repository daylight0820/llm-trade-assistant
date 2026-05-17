# LLM Trade Assistant

> A lightweight AI backend project built with FastAPI + GPT-2 + Retrieval-Augmented Generation (RAG).

一个面向 AI 后端工程学习的 LLM 项目，目标是从“模型调用”逐步演化到“完整 AI 系统工程”。

一个基于 FastAPI + GPT-2 的本地 AI 文本生成与检索增强（RAG）实验项目。

目前项目支持：

* GPT-2 文本生成
* FastAPI API 服务
* 检索增强生成（RAG 雏形）
* 日志记录
* 请求限流
* 健康检查接口
* 模型信息接口

---

# 项目结构

```text
llm-trade-assistant/
│
├── app.py                     # FastAPI 主入口
├── retrieve.py                # 检索逻辑
├── knowledge.txt              # 本地知识库
├── requirements.txt           # Python 依赖
├── Dockerfile                 # Docker 配置
├── .gitignore                 # Git 忽略规则
├── cheatsheet_engineering.md  # 工程速查笔记
└── README.md
```

---

# 项目亮点

* 基于 FastAPI 构建 AI 推理 API
* 使用 GPT-2 实现文本生成
* 支持采样参数控制（temperature / top_p / repetition_penalty）
* 初步实现 Retrieval-Augmented Generation（RAG）
* 支持日志记录与异常处理
* 支持 API 限流（SlowAPI）
* 支持健康检查与模型信息接口
* 面向后续 Docker / 云部署扩展

---

# 系统架构

```text
User Request
     │
     ▼
FastAPI API Layer
     │
     ├── Request Validation
     ├── Rate Limiting
     ├── Logging
     ▼
Retrieval Layer
     │
     ├── Load Knowledge Base
     ├── Retrieve Relevant Context
     ▼
Prompt Construction
     ▼
GPT-2 Generation
     ▼
JSON Response
```

---

# 技术栈

* Python
* FastAPI
* Transformers
* PyTorch
* GPT-2
* Loguru
* SlowAPI

---

# 当前功能

## 1. 文本生成

通过 GPT-2 模型进行文本续写。

支持参数：

* `max_new_tokens`
* `temperature`
* `top_p`
* `repetition_penalty`

---

## 2. 简单 RAG（检索增强生成）

生成前会：

1. 从本地知识库中检索相关内容
2. 拼接到 Prompt 中
3. 再交给 GPT-2 生成

当前为简化版 keyword retrieval。

后续计划升级：

* Embedding
* 向量数据库
* FAISS / Chroma

---

## 3. 限流

使用 SlowAPI 对接口进行限流。

当前限制：

```text
10 requests / minute
```

---

## 4. 日志

使用 Loguru 记录：

* 请求
* 生成结果
* 异常信息

---

# API 接口

## POST /generate

文本生成接口。

### 请求示例

```json
{
  "prompt": "Artificial intelligence",
  "max_new_tokens": 50,
  "temperature": 0.7,
  "top_p": 0.9,
  "repetition_penalty": 1.1
}
```

### 返回示例

```json
{
  "generated_text": "Artificial intelligence is changing the world...",
  "retrieved": [
    "Knowledge chunk 1",
    "Knowledge chunk 2"
  ]
}
```

---

## GET /health

健康检查接口。

### 返回示例

```json
{
  "status": "ok"
}
```

---

## GET /model-info

查看当前模型信息。

### 返回示例

```json
{
  "model": "gpt2-medium",
  "device": "cpu",
  "model_type": "GPT-2 (causal LM)"
}
```

---

# 本地运行

## 1. 创建虚拟环境

Windows:

```bash
python -m venv .venv
```

激活虚拟环境：

```bash
.venv\Scripts\activate
```

---

## 2. 安装依赖

```bash
pip install -r requirements.txt
```

---

## 3. 启动服务

```bash
uvicorn app:app --reload
```

启动后访问：

```text
http://127.0.0.1:8000/docs
```

查看 Swagger API 文档。

---

# 开发路线图

## Stage 1（当前）

* FastAPI API
* GPT-2 推理
* Prompt 增强
* 简单 RAG
* 日志系统
* API 限流

---

## Stage 2（下一步）

* Embedding
* 向量检索
* FAISS / ChromaDB
* 多知识库管理
* Prompt 模板系统
* 模块化项目结构

---

## Stage 3（未来）

* Agent 系统
* Tool Calling
* Redis 缓存
* PostgreSQL
* Docker Compose
* 云服务器部署
* CI/CD
* 前后端分离

---

# GitHub 后续补充

后续计划增加：

* API 截图
* Swagger 文档截图
* 项目架构图
* Docker 部署截图
* RAG 流程图


---

# 后续计划

## 工程方向

* 项目结构拆分
* 日志落盘
* 配置文件管理
* Docker 容器化
* 单元测试
* CI/CD

---

## AI 方向

* 向量检索
* Embedding
* FAISS
* ChromaDB
* 更强的开源模型
* 多轮对话
* Agent

---

# 学习目标

本项目主要用于学习：

* AI Backend Engineering
* LLM API 开发
* RAG 基础
* FastAPI 工程化
* AI 服务部署

---

# 作者备注

这是一个从零开始逐步构建的 AI 工程学习项目。
重点不仅仅只是“让模型跑起来，跑多快”，而是“学会怎么让模型跑起来"
希望从这个项目中学到：
* 工程结构
* API 设计
* 系统思维
* AI 与后端结合
* 可扩展的服务架构
