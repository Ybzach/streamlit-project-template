from src import callbacks
from src.pages import ParserPage
import streamlit as st

st.set_page_config(page_title="Parser Results", layout="wide", initial_sidebar_state="collapsed")

ParserPage.load_page()