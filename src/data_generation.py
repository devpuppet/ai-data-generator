import streamlit as st
from src.service.gemini_service import GeminiAIService
from src.db.db_service import DatabaseService
from io import StringIO
# from dotenv import load_dotenv
# import os

# load_dotenv()

prompt_container = st.container(border=True)
gemini_ai_service = GeminiAIService()

# DB_URL = (
#     f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
#     f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
# )

database_service = DatabaseService()

with prompt_container:
    prompt = st.text_input("Prompt", placeholder="Enter your prompt here")
    upload_ddl_schema_file = st.file_uploader("Upload DDL Schema")
    temperature = st.slider('Temperature')
    max_tokens = st.text_input("Max tokens", value="100")

    def generate():
        if not prompt:
            st.warning("Please enter a prompt")
            return
        if upload_ddl_schema_file is None:
            st.warning("Please select a DDL file")
            return
        schema = StringIO(upload_ddl_schema_file.getvalue().decode("utf-8")).read()
        result = database_service.execute_script(schema)
        response = gemini_ai_service.generate_response(prompt + "\n`" + schema + "`")
        # query = response.text.replace("sql", "")
        # print("QUERY: " + query)
        # result = database_service.execute_query(query)
        # print("DB Result: " + result)

    generate_button = st.button("Generate", on_click=generate)



