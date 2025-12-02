import streamlit as st
from src.container import container
from src.service.generate_options import GenerateOptions
from io import StringIO
import pandas as pd

prompt_container = st.container(border=True)
database_service = container.database_service()
ai_service = container.ai_service()

with prompt_container:
    prompt = st.text_input("Prompt", placeholder="Enter your prompt here")
    upload_ddl_schema_file = st.file_uploader("Upload DDL Schema")
    temperature = st.slider('Temperature', min_value=0.0, max_value=2.0)
    max_tokens = st.text_input("Max tokens", value="1000", max_chars=4)

    def generate():
        if not prompt:
            st.warning("Please enter a prompt")
            return
        if upload_ddl_schema_file is None:
            st.warning("Please select a DDL file")
            return
        schema = StringIO(upload_ddl_schema_file.getvalue().decode("utf-8")).read()
        database_service.create_schema_from_ddl(schema)
        model_response = ai_service.generate_response(prompt, GenerateOptions(temperature=temperature,
                                                                              max_tokens=max_tokens))
        if not model_response.text:
            st.warning(f"An error occured:\n {model_response.error}")
            return
        else:
            st.success(model_response.text)


    generate_button = st.button("Generate", on_click=generate)

data_preview_container = st.container(border=True)

with data_preview_container:
    tables = database_service.get_table_names()
    if not tables:
        st.info("No tables found in the database. Upload a DDL schema first.")
    else:
        table_name = st.selectbox("Select table", tables)
        rows = database_service.select(f"SELECT * FROM {table_name} LIMIT 10;")
        if rows:
            st.table(pd.DataFrame(rows))
        else:
            st.info(f"No rows found in {table_name} table")

        edit_instructions = st.text_input("Edit instructions",
                                          placeholder="Enter quick edit instructions",
                                          label_visibility="collapsed")

    def edit():
        if not edit_instructions:
            st.warning("Please enter edit instructions")
            return
        model_response = ai_service.generate_response(edit_instructions,
                                                      GenerateOptions(temperature=temperature,
                                                                      max_tokens=max_tokens))
        if not model_response.text:
            st.warning(f"An error occured:\n {model_response.error}")
            return
        else:
            st.success(model_response.text)

    edit_button = st.button("Submit", on_click=edit)
