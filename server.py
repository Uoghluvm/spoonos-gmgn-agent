from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from spoon_ai.agents.toolcall import ToolCallAgent
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager
from gmgn_scraper import GmgnScraperTool

app = FastAPI()

class AnalyzeRequest(BaseModel):
    url: str
    api_key: str
    model: str = "gemini-2.5-flash"

@app.post("/analyze")
async def analyze_token(request: AnalyzeRequest):
    try:
        # 1. 动态初始化 ChatBot (使用前端传来的 API Key)
        # 注意：实际生产中不建议每次请求都重新初始化，这里为了演示灵活性
        os.environ["GEMINI_API_KEY"] = request.api_key
        
        chat_bot = ChatBot(
            llm_provider="gemini",
            model_name=request.model
        )

        # 2. 初始化 Agent
        meme_analyst = ToolCallAgent(
            name="MemeCoinAnalyst",
            description="An AI agent that analyzes meme coin fundamentals.",
            system_prompt="You are a crypto analyst. Fetch data using the tool and provide a comprehensive fundamental analysis.",
            available_tools=ToolManager([GmgnScraperTool()]),
            llm=chat_bot
        )

        # 3. 提取地址 (简单处理，Tool 内部会再次校验)
        # 假设 URL 格式: https://gmgn.ai/sol/token/xyz...
        # 我们直接把 URL 给 Agent，让它自己提取或者我们帮它解析
        prompt = f"请分析这个 GMGN 页面对应的代币数据: {request.url}。如果是 Sol/BSC/ETH 地址，请自动识别链类型并抓取。"
        
        print(f"🤖 Agent 收到请求: {prompt}")
        result = await meme_analyst.run(prompt)
        
        return {"status": "success", "analysis": result}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
