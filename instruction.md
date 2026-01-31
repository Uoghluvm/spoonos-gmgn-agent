# 📝 SpoonOS 实战笔记：Web3 Agent (GMGN 数据抓取 + Gemini 分析)

**日期**：2026-01-31
**环境**：Python 3.12 + uv
**核心能力**：Playwright 自动化抓取 -> LLM (Gemini 2.5) 语义分析 -> 结构化研报

## 1. 项目目标

构建一个 AI Agent，能够：
1.  **听懂指令**：用户输入 Token CA (合约地址)。
2.  **获取数据**：自动访问 [GMGN.ai](https://gmgn.ai)，绕过基础反爬，获取 Meme 币的实时交易数据。
3.  **智能分析**：利用 Google Gemini 2.5 Flash 模型，从杂乱的网页文本中提取核心指标（价格、涨跌幅、持有人安全、筹码分布等）。
4.  **输出报告**：生成简明扼要的投资分析摘要。

## 2. 核心架构 (Implementation)

### 2.1 目录结构

```text
SpoonOSgetGMGN/
├── .env                # [私密] 存放 GOOGLE_API_KEY
├── gmgn_scraper.py     # [Tool] 定义 GmgnScraperTool
├── main.py             # [Agent] 定义 MemeCoinAnalyst Agent
├── spoon/              # [Framework] SpoonOS 的模拟 SDK 实现
└── README.md           # 项目文档
```

### 2.2 关键组件

#### A. Tool: `GmgnScraperTool` (Eyes & Hands)
为了解决 GMGN 的动态渲染和反爬问题，我放弃了传统的 HTTP 请求，改用 `Playwright` 无头浏览器。

*   **策略迭代**：
    *   *v1 (失败)*：尝试用 `networkidle` 等待网络空闲，但因 GMGN WebSocket 数据频发导致超时。
    *   *v2 (成功)*：改为 `domcontentloaded` + 固定延时 (5s) 等待 React Hydration，直接抓取 `document.body.innerText`。
*   **安全加固**：增加了对 Solana CA 格式的正则校验，防止恶意 URL 注入。

#### B. LLM: `GeminiFlash` (Brain)
使用 Google 的 `gemini-2.5-flash` 模型。相比本地逻辑解析 HTML，LLM 的优势在于：
*   **抗变动**：网页改版导致 CSS 选择器失效时，只要文本还在，LLM 就能读懂。
*   **语义理解**：能直接理解 "Burnt 🔥 33.5%" 这种非结构化文本的含义。

#### C. Agent: `MemeCoinAnalyst`
通过 `ToolCallAgent` 将 Tool 和 LLM 串联。Agent 接收自然语言指令，通过关键词识别意图，自动调用 Tool 获取数据上下文，最后由 LLM 生成回答。

## 3. 开发实录

### 第一步：环境初始化
使用 `uv` 极速搭建环境：
```bash
uv init . --python 3.12
uv add playwright google-generativeai python-dotenv
uv run playwright install chromium
```

### 第二步：编写 Scraper (`gmgn_scraper.py`)
```python
# 核心逻辑片段
async def execute(self, token_address):
    # ... URL 构造与安全校验 ...
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="Mozilla/5.0...")
        
        await page.goto(url)
        await page.wait_for_timeout(5000) # 等待数据加载
        
        # 粗暴但有效：获取全页文本
        content = await page.evaluate("() => document.body.innerText")
        return content
```

### 第三步：接入 Gemini (`spoon/core/llm.py`)
```python
# 适配 SpoonOS 接口
class GeminiFlash:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def generate(self, prompt):
        return self.model.generate_content(prompt).text
```

### 第四步：从 0 到 1 的主要坑
1.  **Playwright 超时**：GMGN 是即时数据流网站，网络永远不会 "Idle"。解决方案是改用固定延时等待。
2.  **LLM 模型版本**：`google-generativeai` 库对模型名称敏感，最终确认使用 `gemini-2.5-flash` 可用。
3.  **CSS 选择器脆弱性**：最初试图精确解析 DOM 结构，但维护成本高。**Data-Driven via LLM** 是更优解，把解析压力转移给 AI。

## 4. 运行结果示例

用户提问：`帮我看一下这个币 HeLp...`

**Agent 输出报告**：
> **1. Price and Percentage Changes:**
> *   Current Price: $0.0072
> *   1h Change: -7.26% (Short-term bearish)
>
> **2. Safety:**
> *   🔥 LP Burnt: 33.5% (Positive)
> *   ✅ NoMint / NoBlacklist
>
> **3. Holders:**
> *   Total: 118.3K
> *   Top 10 Ratio: 34% (Healthy distribution)

## 5. 总结

SpoonOS 的 "Agentic" 模式（Tool + LLM）在处理 Web3 数据分析时非常强大。我们不再需要为每个网站写死板的爬虫规则，而是给 Agent 一双“眼睛”（浏览器）和一个“大脑”（LLM），让它像人类分析师一样去阅读和总结。

---
*Next Step: 考虑引入 Twitter 舆情分析 Tool，与链上数据交叉验证。*