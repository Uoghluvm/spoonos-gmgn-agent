class ToolCallAgent:
    def __init__(self, name, description, system_prompt, available_tools, llm):
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.available_tools = available_tools
        self.llm = llm

    async def run(self, input_text):
        print(f"Agent {self.name} received: {input_text}")
        
        # Simple mock logic for tool selection (in real world, LLM does this)
        tool_result = None
        if "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC" in input_text:
             for tool in self.available_tools:
                 if tool.name == "get_gmgn_token_data":
                     print(f"Agent deciding to call tool: {tool.name}")
                     tool_result = await tool.execute("HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC")
                     print(f"Tool Output received ({len(tool_result)} chars).")
        
        if tool_result:
            # Now pass the result to the LLM for analysis
            prompt = f"""
            You are a crypto analyst. I will provide you with raw text scraped from a token analysis website (GMGN.ai). 
            Your task is to extract meaningful information and present it in a clean, structured summary.
            
            Focus on:
            1. Price and Percentage Changes (1m, 5m, 1h, 24h)
            2. Market Cap and Liquidity
            3. Volume and Transactions
            4. Key Safety/Security Indicators (Mintable, Burned, etc.)
            5. Holders and Top Holders info
            
            Here is the raw data:
            ---
            {tool_result}
            ---
            
            Please provide a concise analysis.
            """
            print("Sending data to LLM for analysis...")
            response = await self.llm.generate(prompt)
            print("Agent Final Response:")
            print(response)
            return response
            
        return "I am a mock agent. No relevant tool found or triggered."
