from google import genai
from google.genai.types import GenerateContentConfig
from src.service.ai_service import AIService
import logging

from db.db_service import DatabaseService


class GeminiAIService(AIService):
    def __init__(self, database_service: DatabaseService):
        self._database_service = database_service
        # The client gets the API key from the environment variable `GEMINI_API_KEY`.
        self._client = genai.Client()
        self._config = GenerateContentConfig(
            system_instruction="You are a helpful assistant that generate SQL statements",
            tools=[self.select, self.insert]
        )

    def select(self, sql: str):
        return self._database_service.select(sql)

    def insert(self, sql: str):
        self._database_service.insert(sql)

    def generate_response(self, prompt):
        logging.info("Prompt: " + prompt)
        response = self._client.models.generate_content(
            model="gemini-2.5-flash",
            config=self._config,
            contents=prompt)
        logging.info("Response: " + response.text)
        return response
