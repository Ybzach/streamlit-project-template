"""
this is the main module where you set your initial sessions states
and navigate your page with respect to `selected_page` session state
"""

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

# page navigation
HomePage.load_home_page()