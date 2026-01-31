# 🥄 SpoonOS GMGN Analyst

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![SpoonOS](https://img.shields.io/badge/SpoonOS-SDK-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**SpoonOS GMGN Analyst** 是一个基于 [SpoonOS](https://github.com/spoon-os) 官方 SDK 构建的智能体（AI Agent）。它主要用于自动化抓取 [GMGN.ai](https://gmgn.ai) 的加密货币（Meme Coin）实时数据，并利用 **Google Gemini** 模型生成深度的投资研报。

这个项目展示了如何使用 `spoon-ai-sdk` 封装复杂的浏览器自动化任务 (`playwright`)，并将其作为标准工具 (`Tool`) 提供给 LLM 使用。

---

## 🏗️ 架构概览

```mermaid
graph TD
    User[用户指令] -->|输入| Agent[SpoonOS Agent]
    Agent -->|决策| LLM[Google Gemini 2.5]
    LLM -->|调用工具| Scraper[GmgnScraperTool]
    Scraper -->|启动| Browser[Playwright (Headless)]
    Browser -->|访问| Target[GMGN.ai 页面]
    Target -->|返回数据| Scraper
    Scraper -->|结构化文本| Agent
    Agent -->|最终分析| Report[投资研报]
```

## ✨ 核心功能

*   **🕵️ 隐形抓取**: 使用 `Playwright` 模拟真实浏览器行为，绕过基础反爬检测，获取动态渲染的 React 页面数据。
*   **🧠 智能解析**: 不依赖脆弱的 CSS 选择器提取字段，而是抓取网页全文，让 LLM 基于语义理解提取关键信息（价格、持有人、Dev持仓等）。
*   **📊 深度研报**: 自动分析代币的基本面、安全风险（烧池子、黑名单）和市场情绪。
*   **⚡ 极速部署**: 使用 `uv` 包管理器，秒级完成环境搭建。

---

## 🚀 快速开始

### 1. 环境依赖

*   Python 3.12+
*   [uv](https://github.com/astral-sh/uv) (推荐) 或 pip

### 2. 安装项目

```bash
# 1. 克隆仓库
git clone <YOUR_REPO_URL>
cd SpoonOSgetGMGN

# 2. 初始化环境并安装依赖
uv sync

# 3. 安装浏览器内核 (Playwright)
uv run playwright install chromium
```

### 3. 配置密钥

在项目根目录创建 `.env` 文件：

```ini
# .env
# 必填：用于驱动 Agent 的推理能力
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. 运行 Agent

运行默认脚本，分析 `$WIF` 代币：

```bash
uv run main.py
```

---

## 📝 运行效果示例

执行 `main.py` 后，Agent 将自动浏览 GMGN 页面并输出如下分析（以 $WIF 为例）：

```markdown
Testing Agent (Official SDK)...
🥄 SpoonOS Tool: Navigating to https://gmgn.ai/sol/token/EKpQ...cjm...
🥄 SpoonOS Tool: Page loaded, waiting for data hydration...

Based on the data from gmgn.ai for the $WIF (dogwifhat) token:

**Token Overview:**
*   **Name:** dogwifhat ($WIF)
*   **Market Cap:** $281.58M
*   **Current Price:** $0.281
*   **Holders:** 475.2K

**Security & Trustworthiness:**
*   **LP burned:** Yes (0.07% burnt)
*   **Honeypot:** No indication of being a honeypot.
*   **Mintable:** NoMint (Tokens cannot be minted).
*   **Bug Risk:** 0% Rug probability.

**Overall Sentiment:**
The token demonstrates strong underlying security features (NoMint, No Blacklist, 0% DEV holdings). 
Investors should monitor price action closely given the recent selling pressure but the fundamental distribution looks healthy.
```

---

## 📂 项目结构

```
SpoonOSgetGMGN/
├── .env                # 配置文件 (已在 .gitignore 中排除)
├── gmgn_scraper.py     # ✅ 核心: 自定义 Tool 实现 (基于 spoon-ai-sdk)
├── main.py             # ✅ 入口: Agent 编排与执行
├── pyproject.toml      # 依赖管理
└── uv.lock             # 版本锁定
```

## 🛠️ 二次开发指南

### 添加新工具
参考 `gmgn_scraper.py`，继承 `spoon_ai.tools.BaseTool` 并实现 `execute` 方法即可：

```python
from spoon_ai.tools.base import BaseTool, ToolResult

class MyTool(BaseTool):
    name: str = "my_tool"
    async def execute(self, query: str) -> ToolResult:
        # ... logic ...
        return ToolResult(output="result", system="success")
```

## ⚠️ 免责声明

*   **数据合规**: 本工具仅作为技术概念验证（PoC）。在使用抓取功能时，请严格遵守目标网站 ([gmgn.ai](https://gmgn.ai)) 的 `robots.txt` 协议及服务条款。
*   **投资风险**: 加密货币资产（特别是 Meme 币）波动极大。本工具生成的分析报告由 AI 生成，**不构成任何投资建议**。开发者不对因使用本工具导致的任何财产损失负责。

---

*Powered by [SpoonOS](https://spoon.os)*
