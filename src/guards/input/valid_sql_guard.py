from guardrails import Guard
from guardrails.hub import ValidSQL
import logging


class ValidSqlGuard:
    def __init__(self):
        self.__guard = Guard().use(
            ValidSQL(on_fail="reask")
        )

    def validate_sql(self, sql: str):
        try:
            response = self.__guard.validate(sql)
            logging.info(f"SQL Guard response: {response}")
        except Exception as e:
            logging.error(f"SQL Guard validation error: {e}")
            raise e