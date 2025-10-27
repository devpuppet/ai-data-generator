import streamlit as st
from src.service.gemini_service import GeminiAIService

prompt_container = st.container(border=True)
gemini_ai_service = GeminiAIService()

with prompt_container:
    prompt = st.text_input("Prompt", placeholder="Enter your prompt here")
    upload_ddl_schema = st.file_uploader("Upload DDL Schema")
    temperature = st.slider('Temperature')
    max_tokens = st.text_input("Max tokens", value="100")
    generate_button = st.button("Generate", on_click=gemini_ai_service.generate_response, args=(prompt,))
