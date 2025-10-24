import streamlit as st

prompt_container = st.container(border=True)

with prompt_container:
    st.text_input("Prompt", placeholder="Enter your prompt here")
    upload_ddl_schema = st.file_uploader("Upload DDL Schema")
    temperature = st.slider('Temperature')
    max_tokens = st.text_input("Max tokens", value="100")
    generate_button = st.button("Generate")
