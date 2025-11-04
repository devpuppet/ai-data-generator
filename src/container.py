from service.ai_service import AIService
from src.db.db_service import DatabaseService
from src.service.gemini_service import GeminiAIService


class Container:
    def __init__(self):
        self._database_service = DatabaseService()

    def database_service(self) -> DatabaseService:
        return self._database_service

    def ai_service(self) -> AIService:
        return GeminiAIService(self._database_service)


container = Container()
