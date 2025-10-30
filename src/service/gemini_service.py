from google import genai
from google.genai.types import GenerateContentConfig
from src.db.db_service import DatabaseService
import logging

db_service = DatabaseService()

def select(sql: str):
    return db_service.select(sql)


def insert(sql: str):
    db_service.insert(sql)


class GeminiAIService:
    def __init__(self):
        # The client gets the API key from the environment variable `GEMINI_API_KEY`.
        self.__client = genai.Client()
        self.__config = GenerateContentConfig(
            system_instruction="You are a helpful assistant that generate SQL statements",
            tools=[select, insert]
        )

    def generate_response(self, prompt):
        logging.info("Prompt: " + prompt)
        response = self.__client.models.generate_content(
            model="gemini-2.5-flash",
            config=self.__config,
            contents=prompt)
        logging.info("Response: " + response.text)
        return response
