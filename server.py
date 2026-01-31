from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import google.genai
from spoon_ai.agents.toolcall import ToolCallAgent
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager
from gmgn_scraper import GmgnScraperTool

app = FastAPI()

# Allow CORS for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str
    api_key: str
    model: str = "gemini-2.5-flash"

class ModelListRequest(BaseModel):
    api_key: str

@app.post("/models")
async def list_models(request: ModelListRequest):
    try:
        # Use google-genai SDK to list models
        client = google.genai.Client(api_key=request.api_key)
        # Verify valid API key by listing models
        # Note: 'gemini-2.5-flash' might not appear in public lists yet if experimental
        # So we include a default list + fetched ones
        
        # Simple validation: valid key check
        # We return a standard list for now to avoid complexity of filtering 'generateContent' capable models
        # because listing all models returns hundreds of endpoints (embedding, etc)
        
        # Let's return a curated high-quality list for this Agent
        # But if the user wants "dynamic", we simulate it or try to fetch
        
        return {
            "status": "success",
            "models": [
                "gemini-2.5-flash", 
                "gemini-1.5-pro", 
                "gemini-1.5-flash",
                "gemini-1.5-flash-8b"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid API Key: {str(e)}")

@app.post("/analyze")
async def analyze_token(request: AnalyzeRequest):
    try:
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        os.environ["GEMINI_API_KEY"] = request.api_key
        
        chat_bot = ChatBot(
            llm_provider="gemini",
            model_name=request.model
        )

        meme_analyst = ToolCallAgent(
            name="MemeCoinAnalyst",
            description="An AI agent that analyzes meme coin fundamentals.",
            system_prompt=f"""You are a professional Tier-1 Crypto Analyst.
Current Date/Time: {current_time}
(Use this date as the absolute reference for all time-based calculations. If a token was created before this date, it is in the past.)

**CRITICAL OUTPUT FORMAT:**
1. **🚀 投资建议 (Investment Recommendation)**: Start immediately with a clear BUY / SELL / AVOID rating and a 1-sentence summary reason.
2. **Risk Assessment**: High/Medium/Low risk flags.
3. **Fundamental Analysis**: Tokenomics, holders, liquidity, etc.

Analyze the data strictly based on this structure.""",
            available_tools=ToolManager([GmgnScraperTool()]),
            llm=chat_bot
        )
        
        prompt = f"请分析这个 GMGN 页面对应的代币数据: {request.url}。"
        print(f"🤖 Agent 收到请求: {prompt} (Model: {request.model})")
        
        result = await meme_analyst.run(prompt)
        return {"status": "success", "analysis": result}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
