from google import genai
import logging


class GeminiAIService:
    def __init__(self):
        # The client gets the API key from the environment variable `GEMINI_API_KEY`.
        self.__client = genai.Client()

    def generate_response(self, prompt):
        logging.info("Prompt: " + prompt)
        response = self.__client.models.generate_content(model="gemini-2.5-flash",
                                                         contents=prompt)
        logging.info("Response: " + response.text)
        return response
