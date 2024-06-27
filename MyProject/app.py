import streamlit as st
from src.pages import HomePage, ParserPage
from text_segmentation.resume_segment import resumeSegmenter
# from streamlit-extras import switch_page

# page config
st.set_page_config(page_title="Resume Analysis", layout="centered", initial_sidebar_state="collapsed")


# set session states
if 'selected_page' not in st.session_state:
    st.session_state['submitted'] = False
if 'resume' not in st.session_state:
    st.session_state['resume'] = None
if 'analysis' not in st.session_state:
    st.session_state['analysis'] = 'input'
if 'segment_results' not in st.session_state:
    st.session_state['segment_results'] = {}
if 'entities' not in st.session_state:
    st.session_state['entities'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'initial_analysis' not in st.session_state:
    st.session_state['initial_analysis'] = ""
if 'openai_api_key' not in st.session_state:
    st.session_state['openai_api_key'] = None

# page navigation
HomePage.load_home_page()