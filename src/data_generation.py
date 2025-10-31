import streamlit as st
from src.container import container
from io import StringIO


prompt_container = st.container(border=True)
database_service = container.database_service()
gemini_ai_service = container.gemini_service()


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
        result = database_service.create_schema_from_ddl(schema)
        response = gemini_ai_service.generate_response(prompt + "\n`" + schema + "`")

    generate_button = st.button("Generate", on_click=generate)



