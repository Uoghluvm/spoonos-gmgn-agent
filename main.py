import asyncio
import os
from dotenv import load_dotenv
from spoon_ai.agents.toolcall import ToolCallAgent
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager
from gmgn_scraper import GmgnScraperTool

# Load environment variables
load_dotenv()

async def main():
    # Official SDK uses ChatBot factory
    chat_bot = ChatBot(
        llm_provider="gemini", 
        model_name="gemini-2.5-flash"
    )

    meme_analyst = ToolCallAgent(
        name="MemeCoinAnalyst",
        description="An AI agent that analyzes meme coin fundamentals.",
        system_prompt="You are a crypto analyst. When asked about a token, use the 'get_gmgn_token_data' tool to fetch live data, then summarize the sentiment.",
        available_tools=ToolManager([GmgnScraperTool()]),
        llm=chat_bot
    )

    # Test Run
    print("Testing Agent (Official SDK)...")
    result = await meme_analyst.run("帮我看一下这个币的数据：HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
