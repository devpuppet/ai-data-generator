from src.db.db_service import DatabaseService
from src.service.gemini_service import GeminiAIService


class Container:
    def __init__(self):
        self._database_service = DatabaseService()
        self._gemini_service = GeminiAIService(self._database_service)

    def database_service(self):
        return self._database_service

    def gemini_service(self):
        return self._gemini_service


container = Container()
