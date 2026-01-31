# 🥄 SpoonOS GMGN Analyst

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![SpoonOS](https://img.shields.io/badge/SpoonOS-SDK-green.svg)
![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-googlechrome.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**SpoonOS GMGN Analyst** 是一个基于 [SpoonOS](https://xspoonai.github.io/) 官方 SDK 构建的 AI Agent 工具套件。

它不仅提供开发者友好的 Python CLI 工具，更包含一个强大的 **Chrome 侧边栏插件**，让你在浏览 [GMGN.ai](https://gmgn.ai) 时，一键调用 **Google Gemini** 模型生成深度的基本面投资研报。

---

## 🏗️ 架构模式

本项目的核心是一个本地运行的智能体服务 (`Server`)，通过 Chrome 插件或 CLI 接收指令。

```mermaid
graph LR
    subgraph Browser [Chrome 浏览器]
        User[用户] -->|点击分析| Ext[侧边栏插件 (SidePanel)]
        Ext -->|获取当前 URL| Tab[当前页面 (GMGN)]
    end
    
    subgraph LocalHost [本地环境]
        Ext -->|POST /analyze| Server[FastAPI Server]
        Server -->|调度| Agent[SpoonOS Agent]
        Agent -->|调用| LLM[Google Gemini 2.5]
        Agent -->|启动| Scraper[Playwright Tool]
    end
    
    Scraper -->|抓取数据| Tab
    Agent -->|Markdown 研报| Ext
    Ext -->|渲染展示| User
```

## ✨ 核心功能

*   **🧩 浏览器无缝集成**: 独家提供 Chrome 侧边栏插件，无需离开交易界面即可获得分析。
*   **📝 Markdown 完美渲染**: 研报支持富文本渲染（加粗、列表、代码块），阅读体验极佳。
*   **🌐 全链支持**: 完美支持 **Solana, BSC, ETH, Base, Tron** 等主流公链代币分析。
*   **🧠 深度逻辑**:
    *   **结论先行**: 报告开头直接给出 **BUY / SELL / AVOID** 评级。
    *   **风险识别**: 自动检测貔貅盘、烧池子、黑名单及 DEV 持仓风险。
*   **⚙️ 动态模型**: 支持在插件端动态切换 `gemini-2.5-flash`, `gemini-1.5-pro` 等模型。

---

## 🚀 快速开始

### 1. 环境准备

确保安装了 [uv](https://github.com/astral-sh/uv) (极速 Python 包管理器)。

```bash
git clone <YOUR_REPO_URL>
cd SpoonOSgetGMGN
uv sync
uv run playwright install chromium
```

### 2. 方式一：使用 Chrome 插件 (推荐) 🔥

**步骤 A: 启动本地服务**
在终端运行 Agent 服务：
```bash
uv run server.py
# 服务将运行在 http://localhost:8000
```

**步骤 B: 安装插件**
1.  打开 Chrome 浏览器，输入 `chrome://extensions/`。
2.  开启右上角 **"开发者模式" (Developer mode)**。
3.  点击 **"加载已解压的扩展程序" (Load unpacked)**。
4.  选择本项目下的 `extension` 目录。

**步骤 C: 开始使用**
1.  打开任意 [GMGN.ai](https://gmgn.ai) 代币详情页。
2.  点击浏览器侧边栏图标，选择 **SpoonOS GMGN Analyst**。
3.  输入你的 `GEMINI_API_KEY` (自动保存)。
4.  点击 **Analyze Page**，等待 30-60 秒即可获取研报！

### 3. 方式二：使用 CLI (开发者调试)

如果您想直接测试 Agent 逻辑或进行二次开发，可以使用 CLI 模式：

```bash
# 1. 配置环境变量
echo "GEMINI_API_KEY=your_key" > .env

# 2. 运行脚本 (默认分析 $WIF)
uv run main.py
```

---

## 🛠️ 项目结构

```
SpoonOSgetGMGN/
├── extension/          # 🧩 Chrome 插件源码
│   ├── manifest.json   # 插件配置
│   ├── sidepanel.html  # 侧边栏 UI
│   ├── sidepanel.js    # 插件逻辑 (Fetch API)
│   └── marked.min.js   # Markdown 渲染引擎
├── server.py           # 🚀 后端服务 (FastAPI + SpoonOS Agent)
├── gmgn_scraper.py     # 🕷️ 核心工具 (Playwright 抓取)
├── main.py             # 🧪 CLI 测试入口
├── pyproject.toml      # 📦 依赖配置
└── README.md           # 📄 说明文档
```

## ⚠️ 免责声明

*   **数据合规**: 本工具仅作为技术概念验证（PoC）。请严格遵守目标网站的使用条款。
*   **投资风险**: 加密货币资产（特别是 Meme 币）波动极大。本工具生成的分析报告由 AI 生成，**不构成任何投资建议**。开发者不对因使用本工具导致的任何财产损失负责。

---

*Powered by [SpoonOS](https://xspoonai.github.io/)*
