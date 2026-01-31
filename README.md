# 🥄 SpoonOS GMGN Scraper & Analyst

这是一个基于 **SpoonOS** 概念验证的 AI Agent 工具，旨在自动化抓取 [GMGN.ai](https://gmgn.ai) 的实时 Meme 币数据，并利用 Google Gemini 模型进行深度的基本面分析。

## ✨ 功能特点

*   **智能抓取 (Smart Scraping)**: 集成 `Playwright` 自动化浏览器，能够处理 GMGN 的动态渲染和数据高频刷新。
*   **抗反爬设计**: 模拟真实用户行为，绕过基础的自动化检测。
*   **AI 深度分析**: 抓取页面原始数据后，通过 **Google Gemini 2.5 Flash** 模型进行语义分析，提取关键指标（价格、流动性、持有人结构、安全风险等）。
*   **结构化输出**: 将杂乱的网页文本转化为清晰的结构化投资研报。

## 🛠️ 技术栈

*   **Python 3.12**
*   **uv**: 极速 Python 包管理器
*   **Playwright**: 浏览器自动化
*   **SpoonOS SDK**: 官方 AgentOS 框架
*   **Google Gemini API**: 本地 LLM 推理

## 🚀 快速开始

### 1. 环境准备

确保你已经安装了 [uv](https://github.com/astral-sh/uv)。

### 2. 克隆项目与安装依赖

```bash
git clone <your-repo-url>
cd SpoonOSgetGMGN

# 初始化环境并安装依赖 (uv 会自动处理)
uv sync
```

### 3. 安装浏览器引擎

Playwright 需要下载对应的浏览器内核：

```bash
uv run playwright install chromium
```

### 4. 配置环境变量

在项目根目录下创建一个 `.env` 文件，并填入你的 Google Gemini API Key：

```bash
# .env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. 运行 Agent

运行主程序来测试 Agent：

```bash
uv run main.py
```

## 📂 项目结构

```
SpoonOSgetGMGN/
├── .env                # 环境变量 (不要上传!)
├── .gitignore
├── gmgn_scraper.py     # 核心抓取工具 (Tool) - 基于 spoon-ai-sdk
├── main.py             # 入口文件，定义 Agent 和流程
├── pyproject.toml      # 项目依赖配置
└── uv.lock
```

## ⚠️ 免责声明

本项目仅供学习和研究使用。
*   抓取数据请遵守目标网站的 `robots.txt` 协议和使用条款。
*   投资加密货币（尤其是 Meme 币）具有极高风险，本工具生成的分析仅供参考，不构成任何投资建议。

## 🤝 贡献

欢迎提交 Issue 和 PR 改进这个 Agent！
