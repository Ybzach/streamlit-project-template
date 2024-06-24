"""
this is where you define your callbacks
"""

import streamlit as st
from src import components

def set_resume(document):
    st.session_state['resume'] = document

def get_resume():
    return st.session_state['resume']

def load_parser():
    components.parser_ui()

def update_submit(submitted: bool):
    st.session_state['submitted'] = submitted 

def segment_resume(resume):
    st.session_state['segmenter'].segment(resume)
    
def get_segment():
    return st.session_state['segmenter'].results