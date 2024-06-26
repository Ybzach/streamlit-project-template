from src import callbacks
from src.pages import ChatPage
import streamlit as st

st.set_page_config(page_title="Analysis Results", layout='wide', initial_sidebar_state="collapsed")

ChatPage.load_page()