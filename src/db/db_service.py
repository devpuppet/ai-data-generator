from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ResourceClosedError
from dotenv import load_dotenv
import os
import logging


class DatabaseService:
    def __init__(self):
        load_dotenv()
        DB_URL = (
            f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
        print("DB URL: " + DB_URL)
        self.engine = create_engine(DB_URL)
        self.Session = sessionmaker(bind=self.engine)

    def insert(self, query: str, params=None):
        with self.engine.begin() as conn:
            conn.execute(text(query), params or {})

    def select(self, query: str, params=None):
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return result.fetchall()
        # with self.engine.connect() as conn:
        #     try:
        #         result = conn.execute(text(query), params or {})
        #         try:
        #             return result.fetchall()
        #         except ResourceClosedError:
        #             return None
        #     except Exception as e:
        #         logging.error(f"Error executing SQL:\n{query}\n{e}")
        #         raise

    def execute_script(self, sql_script: str):
        """Execute multiple SQL statements in order (split by semicolon)."""
        # naive split is fine for typical DDL (no semicolons inside literals)
        statements = [s.strip() for s in sql_script.split(';') if s.strip()]
        with self.engine.begin() as conn:  # begin() opens a transaction and commits/rolls back
            for stmt in statements:
                try:
                    conn.execute(text(stmt))
                except Exception as e:
                    logging.error(f"Error executing statement:\n{stmt}\n{e}")
