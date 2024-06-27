"""
this is where you define your callbacks
"""

import streamlit as st
from src import components
from text_segmentation.resume_segment import resumeSegmenter
from information_extraction import inference as pipeline

def set_resume(document):
    st.session_state['resume'] = document

def get_resume():
    return st.session_state['resume']

def load_parser():
    components.parser_ui()

def update_submit(submitted: bool):
    st.session_state['submitted'] = submitted 

def segment_resume():
    with st.spinner('Parsing Resume...'):
        segmenter = resumeSegmenter()
        resume = get_resume()
        results = segmenter.segment(resume)
        set_segment_results(results)
    
def get_segment_results():
    return st.session_state['segment_results']

def set_segment_results(results):
    st.session_state['segment_results'] = results

def get_entities():
    return st.session_state['entities']

def save_job_description(job_description):
    st.session_state['job_description'] = job_description

@st.cache_resource(show_spinner=False)
def load_ner_model():
    print("Loading NER model...")
    return pipeline.Predictor()


def analyse_job_description():
    print("Analyzing job description...")
    with st.spinner("Analysing job description..."):
        ner_model = load_ner_model()
        print("NER model loaded successfully...")
        job_description = st.session_state['job_description']

        st.session_state['entities'] = ner_model.ner_predict(job_description)

def set_openai_api_key(api_key):
    st.session_state['openai_api_key'] = api_key

def get_openai_api_key():
    return st.session_state['openai_api_key']