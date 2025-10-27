import streamlit as st
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

data_generation = st.Page("data_generation.py", title = "Data Generation")
talk_to_your_data = st.Page("talk_to_your_data.py", title = "Talk to your data")

pg = st.navigation([data_generation, talk_to_your_data])

pg.run()

