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
        """Executes SQL SELECT query to read the data from the database

        Args:
            sql (str): SQL SELECT query
        Returns:
            List[Dict]: returns list of dictionaries
        """
        return self._database_service.select(sql)

    def insert(self, sql: str):
        """Executes SQL INSERT query to add new data to the database

        Args:
            sql (str): SQL INSERT query
        Returns:
            None: returns nothing
        """
        self._database_service.insert(sql)

    def update(self, sql: str):
        """Executes SQL UPDATE query to modify data in the database

        Args:
            sql (str): SQL UPDATE query
        Returns:
            None: returns nothing
        """
        self._database_service.update(sql)

    def get_tables(self):
        """Executes SQL SELECT query to get all table names in the database

        Args:
            None
        Returns:
            None: returns list of table names
        """
        return self._database_service.get_table_names()

    def get_table_schema(self, table_name: str):
        """Executes SQL query to get the full database schema

        Args:
            table_name (str): table name
        Returns:
            None: object containing schema for the given table
        """
        return self._database_service.get_table_schema(table_name)

    def generate_response(self, prompt: str, options: GenerateOptions):
        logging.info("Prompt: " + prompt)

        tools = [self.select, self.insert, self.update, self.get_tables, self.get_table_schema]
        config = GenerateContentConfig(
            system_instruction="You are a helpful assistant that generate SQL statements. When generating SQL statements, follow below instructions:\n"
                               "1. Use SELECT queries on other tables to get values for foreign keys\n"
                               "2. To get all available tables, use get_tables tool\n"
                               "3. If you need to know table schema, use get_table_schema tool",
            tools=tools,
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
        try:
            if getattr(response, "text", None):
                return response.text

            candidates = getattr(response, "candidates", None)
            if candidates and len(candidates) > 0:
                candidate = candidates[0]
                content = getattr(candidate, "content", None)

                if content and getattr(content, "parts", None):
                    first_part = content.parts[0]
                    return getattr(first_part, "text", "<no text in part>")

            logging.warning(f"No text content found in Gemini response: {response}")
            return "<no text in response>"

        except Exception as e:
            logging.error(f"Error parsing response: {e}")
            return f"<error extracting text: {e}>"
