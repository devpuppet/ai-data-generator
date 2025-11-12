from google import genai
from google.genai.types import GenerateContentConfig
from google.genai.errors import APIError, ServerError
from src.service.ai_service import AIService
from .generate_options import GenerateOptions
import logging

from db.db_service import DatabaseService
from .model_response import ModelResponse


class GeminiAIService(AIService):
    def __init__(self, database_service: DatabaseService):
        self._database_service = database_service
        # The client gets the API key from the environment variable `GEMINI_API_KEY`.
        self._client = genai.Client()

    def select(self, sql: str):
        return self._database_service.select(sql)

    def insert(self, sql: str):
        self._database_service.insert(sql)

    def generate_response(self, prompt: str, options: GenerateOptions):
        logging.info("Prompt: " + prompt)

        config = GenerateContentConfig(
            system_instruction="You are a helpful assistant that generate SQL statements",
            tools=[self.select, self.insert],
            temperature=options.temperature,
            max_output_tokens=options.max_tokens
        )

        try:
            response = self._client.models.generate_content(
                model="gemini-2.5-flash",
                config=config,
                contents=prompt)
            logging.info("Response: " + self.getResponseText(response))
            return ModelResponse(text=self.getResponseText(response))

        except ServerError as e:
            logging.error(f"Server error: {e}")
            return ModelResponse(error=f"Server error: {e}")

        except APIError as e:
            logging.error(f"API error: {e}")
            return ModelResponse(error=f"API error: {e}")

        except Exception as e:
            logging.exception("Unexpected error during generation")
            return ModelResponse(error=f"Unexpected error: {e}")

    def getResponseText(self, response):
        if response.text:
            output_text = response.text
        elif response.candidates and response.candidates[0].content.parts:
            output_text = response.candidates[0].content.parts[0].text
        else:
            output_text = "<no text in response>"

        return output_text
