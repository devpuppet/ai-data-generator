from guards.input.valid_sql_guard import ValidSqlGuard
from service.ai_service import AIService
from src.db.db_service import DatabaseService
from src.service.gemini_service import GeminiAIService
from dotenv import load_dotenv
import os


class Container:
    def __init__(self):
        load_dotenv()
        db_url = (
            f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
        self._database_service = DatabaseService(db_url)
        self.__valid_sql_guard = ValidSqlGuard()

    def database_service(self) -> DatabaseService:
        return self._database_service

    def valid_sql_guard(self) -> ValidSqlGuard:
        return self.__valid_sql_guard

    def ai_service(self) -> AIService:
        return GeminiAIService(self._database_service, self.__valid_sql_guard)


container = Container()
