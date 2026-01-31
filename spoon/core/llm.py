import google.generativeai as genai
import os

class OpenAIGpt4:
    def __init__(self, api_key):
        self.api_key = api_key

    async def generate(self, prompt):
        return "Mock GPT-4 Response"

class GeminiFlash:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash') # Using a flash model

    async def generate(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating content with Gemini: {e}"

