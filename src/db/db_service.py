from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging
import re


class DatabaseService:
    def __init__(self, DB_URL: str):
        self.engine = create_engine(DB_URL)
        self.Session = sessionmaker(bind=self.engine)

    def insert(self, query: str, params=None):
        self.execute_statement(query, params)

    def update(self, query: str, params=None):
        self.execute_statement(query, params)

    def select(self, query: str, params=None):
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return [dict(row._mapping) for row in result.fetchall()]

    def execute_statement(self, query: str, params=None):
        try:
            with self.engine.begin() as conn:
                conn.execute(text(query), params or {})
        except SQLAlchemyError as e:
            orig = getattr(e, "orig", None)
            message = str(orig) if orig else str(e)
            logging.error(message)
            raise e

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

    def get_table_schema(self, table_name: str):
        columns = self.get_table_columns(table_name)
        foreign_keys = self.get_table_foreign_keys(table_name)
        schema = {
            "columns": columns,
            "foreign_keys": [
                {
                    "column": fk["column_name"],
                    "references_table": fk["foreign_table_name"],
                    "references_column": fk["foreign_column_name"],
                }
                for fk in foreign_keys
            ]
        }

        return schema

    def get_table_columns(self, table_name: str):
        return self.select(f"""
                    SELECT column_name,
                    data_type,
                    is_nullable,
                    is_identity,
                    identity_generation
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                      AND table_name = '{table_name}'
                """)

    def get_table_foreign_keys(self, table_name: str):
        return self.select(f"""
                        SELECT
                            kcu.column_name AS column_name,
                            ccu.table_name AS foreign_table_name,
                            ccu.column_name AS foreign_column_name
                        FROM 
                            information_schema.table_constraints AS tc
                        JOIN information_schema.key_column_usage AS kcu
                            ON tc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage AS ccu
                            ON ccu.constraint_name = tc.constraint_name
                        WHERE 
                            tc.constraint_type = 'FOREIGN KEY'
                            AND tc.table_schema = 'public'
                            AND tc.table_name = '{table_name}';
                    """)

