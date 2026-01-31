from spoon_ai.tools import BaseTool
from playwright.async_api import async_playwright
import json

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
                "description": "The Solana contract address (CA) of the token."
            }
        },
        "required": ["token_address"]
    }

    async def execute(self, token_address: str):
        # 简单的安全校验：Solana 地址通常是 Base58 编码，长度 32-44
        import re
        if not re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', token_address):
            return "Error: Invalid Solana token address format."

        url = f"https://gmgn.ai/sol/token/{token_address}"
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
                
                # 截取前 4000 字符 (视 Context Window 而定，或者全部返回)
                # 这里返回全部，由 Agent 自行决定如何处理
                return cleaned_content

                
            except Exception as e:
                return f"Error scraping GMGN: {str(e)}"
            finally:
                await browser.close()
