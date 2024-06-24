"""
this is where you define your callbacks
"""

import streamlit as st
from src import components
from lib.util import resume_segment

def set_resume(document):
    st.session_state['resume'] = document

def get_resume():
    return st.session_state['resume']

def load_parser():
    components.parser_ui()

def update_submit(submitted: bool):
    st.session_state['submitted'] = submitted 

def segment_resume(resume):
    results = st.session_state['segmenter'].segment(resume)
    set_segment_results(results)

def reload_segmenter():
    st.session_state['segmenter'] = resume_segment.resumeSegmenter()
    
def get_segment_results():
    return st.session_state['segment_results']

def set_segment_results(results):
    st.session_state['segment_results'] = results