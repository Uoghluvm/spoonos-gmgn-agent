import asyncio
import os
from dotenv import load_dotenv
from spoon.core.agents import ToolCallAgent
from spoon.core.llm import OpenAIGpt4, GeminiFlash
from gmgn_scraper import GmgnScraperTool

# Load environment variables
load_dotenv()

async def main():
    # Initialize Agent with Gemini
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env")
        return

    meme_analyst = ToolCallAgent(
        name="MemeCoinAnalyst",
        description="An AI agent that analyzes meme coin fundamentals.",
        system_prompt="You are a crypto analyst.",
        available_tools=[GmgnScraperTool()],
        llm=GeminiFlash(api_key=api_key)
    )

    # Test Run
    print("Testing Agent...")
    # Using the CA from the instruction which is HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC (Use a real one if I want it to work? No, this is fine for test, though it might not exist if it was hypothetical)
    # The instruction says "Assume it is a popular Meme CA".
    # I'll stick to the one in the instruction.
    input_instruction = "帮我看一下这个币的数据：HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"
    await meme_analyst.run(input_instruction)

if __name__ == "__main__":
    asyncio.run(main())
