from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import logging
import re


class DatabaseService:
    def __init__(self):
        load_dotenv()
        DB_URL = (
            f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
        self.engine = create_engine(DB_URL)
        self.Session = sessionmaker(bind=self.engine)

    def insert(self, query: str, params=None):
        self.execute_statement(query, params)

    def select(self, query: str, params=None):
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return [dict(row._mapping) for row in result.fetchall()]

    def execute_statement(self, query: str, params=None):
        with self.engine.begin() as conn:
            conn.execute(text(query), params or {})

    def create_schema_from_ddl(self, sql_script: str):
        statements = self.split_script_to_statements(sql_script)

        for statement in statements:
            statement_lower = statement.lower()
            if "create type" in statement_lower:
                self.create_type_if_doesnt_exist(statement)
            elif "create table" in statement_lower:
                self.create_table_if_doesnt_exist(statement)
            else:
                try:
                    self.execute_statement(statement)
                except Exception as e:
                    logging.warning(f"Skipping statement due to error:\n{statement}\n{e}")

    def split_script_to_statements(self, sql_script: str):
        return [s.strip() for s in sql_script.split(';') if s.strip()]

    def create_type_if_doesnt_exist(self, sql_type_create_statement: str):
        type_name = self.extract_type_name(sql_type_create_statement)
        try:
            exist = self.does_type_exist(type_name)
            if exist:
                logging.info(f"Type '{type_name}' already exists, skipping creation.")
            else:
                self.execute_statement(sql_type_create_statement)
                logging.info(f"Type '{type_name}' created successfully.")
        except Exception as e:
            logging.error(f"Error checking existing type:\n{type_name}\n{e}")

    def extract_type_name(self, sql_create_statement):
        match = re.search(r"CREATE\s+TYPE\s+([a-zA-Z_][a-zA-Z0-9_]*)", sql_create_statement, re.IGNORECASE)
        if not match:
            logging.error(f"Could not extract type name from SQL:\n{sql_create_statement}")
            return None
        return match.group(1)

    def does_type_exist(self, type_name: str):
        exists_check = f"""
                    SELECT 1 FROM pg_type WHERE typname = '{type_name.lower()}';
                    """
        return self.select(exists_check)

    def create_table_if_doesnt_exist(self, sql_create_statement: str):
        if "if not exists" not in sql_create_statement.lower():
            sql_create_statement = sql_create_statement.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
        self.execute_statement(sql_create_statement)
        logging.info(f"Executed: {sql_create_statement.splitlines()[0][:60]}...")

    def get_table_names(self):
        query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_type = 'BASE TABLE'
                ORDER BY table_name; \
                """
        rows = self.select(query)
        return [r["table_name"] for r in rows]
