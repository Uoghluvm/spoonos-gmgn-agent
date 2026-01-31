from spoon_ai.tools.base import BaseTool, ToolResult
from playwright.async_api import async_playwright
import json
from typing import Any, Dict

class GmgnScraperTool(BaseTool):
    # Tool 的唯一标识符，Agent 通过这个名字调用
    name: str = "get_gmgn_token_data"
    
    # 描述 Tool 的功能，Prompt Engineering 的一部分
    description: str = "Fetches real-time token data (price, volume, holders) from gmgn.ai for a given Solana token address."
    
    # 定义参数结构 (JSON Schema)
    parameters: dict = {
        "type": "object",
        "properties": {
            "token_address": {
                "type": "string",
                "description": "The contract address (CA) of the token, OR the full GMGN.ai URL (e.g., https://gmgn.ai/sol/token/xyz)."
            },
            "chain": {
                "type": "string",
                "enum": ["sol", "bsc", "eth", "base", "blast", "tron"],
                "default": "sol",
                "description": "The blockchain network code. Ignored if a full URL is provided."
            }
        },
        "required": ["token_address"]
    }

    async def execute(self, token_address: str, chain: str = "sol") -> ToolResult:
        import re
        
        # 1. URL Mode
        if token_address.startswith("http"):
            url = token_address
            # Optional: Extract chain/address for logging or validation, but we trust the URL primarily
            print(f"🥄 SpoonOS Tool: Using direct URL: {url}")
            # Basic validation to ensure it's gmgn
            if "gmgn.ai" not in url:
                 return ToolResult(error="Error: The provided URL is not a valid GMGN.ai URL.")
        else:
            # 2. Address Mode (Legacy)
            # 链与地址格式的校验逻辑
            is_evm = chain in ["bsc", "eth", "base", "blast"]
            is_sol = chain == "sol"
            is_tron = chain == "tron"

            valid = False
            if is_sol:
                # Solana: Base58, 32-44 chars
                if re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', token_address):
                    valid = True
            elif is_evm:
                # EVM: Hex, starts with 0x, 42 chars total
                if re.match(r'^0x[a-fA-F0-9]{40}$', token_address):
                    valid = True
            elif is_tron:
                # Tron: Starts with T, 34 chars
                if re.match(r'^T[a-zA-Z0-9]{33}$', token_address):
                    valid = True
            
            if not valid:
                return ToolResult(error=f"Error: Invalid token address format for chain '{chain}'.")

            url = f"https://gmgn.ai/{chain}/token/{token_address}"
            print(f"🥄 SpoonOS Tool: Constructed URL {url} from address")
        
        # Common Scraper Logic
        print(f"🥄 SpoonOS Tool: Navigating to {url}...")
        
        async with async_playwright() as p:
            # 启动无头浏览器，设置 User-Agent 规避基础反爬
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            try:
                # 访问页面
                # GMGN 数据频繁刷新，networkidle 容易超时
                # 改为等待 DOM 加载完成 + 固定延时等待数据渲染
                await page.goto(url, timeout=60000)
                await page.wait_for_load_state("domcontentloaded")
                print("🥄 SpoonOS Tool: Page loaded, waiting for data hydration...")
                await page.wait_for_timeout(5000) # 等待 5 秒让 React 渲染和数据填充

                # 模拟用户滚动以触发懒加载（如果需要）
                # await page.mouse.wheel(0, 500)
                
                # --- 获取页面可见文本内容 ---
                # 直接获取 body.innerText，让 LLM 去做结构化分析
                content = await page.evaluate("() => document.body.innerText")
                
                # 简单清洗：去除过多空行
                cleaned_content = "\n".join([line.strip() for line in content.split('\n') if line.strip()])
                
                return ToolResult(
                    output=cleaned_content,
                    system="Successfully scraped GMGN data."
                )
                
            except Exception as e:
                return ToolResult(error=f"Error scraping GMGN: {str(e)}")
            finally:
                await browser.close()
