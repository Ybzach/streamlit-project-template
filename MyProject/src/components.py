"""
this is where you define your components
every component is a piece of row of your application
"""

import streamlit as st
from src import callbacks
from streamlit_javascript import st_javascript
import pandas as pd
import time
import base64
from openai import OpenAI
from langchain.prompts import PromptTemplate

def home_title():
    st.title('End-to-End Resume Analysis with LLM :brain:')

def display_pdf(upl_file, width):
    # Read file as bytes:
    bytes_data = upl_file.getvalue()

    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode("utf-8", 'ignore')

    # Embed PDF in HTML
    pdf_display = f'''
    <style>.block-container{{
        padding-top:2rem;
    }}
    </style>
    <iframe src="data:application/pdf;base64,{base64_pdf}" width={str(width)} height={str(width*4/3)} type="application/pdf"></iframe>
    '''

    home_button = st.button('Upload Resume Again')
    if home_button:
        callbacks.update_submit(False)
        st.switch_page('app.py')
    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)

def pdf_uploader():
    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"],
        help="Only PDF files are supported",
    )
    try:
        if uploaded_file: 
            callbacks.set_resume(uploaded_file)
            
            callbacks.update_submit(True)
    except:
        st.error('Upload failed, please try again.', icon="🚨")

def display_results(results):
    results_df = pd.DataFrame.from_dict(results, orient="index").reset_index()
    results_df = results_df.rename(columns={"index": "Section", 0: "Content"})
    
    with st.form("segmenter_editor_form"):
        st.title("Parser Results")
        st.caption("Double click on the content cells to edit the results as needed.")
        edited_segment = st.data_editor(
                results_df,
                hide_index=True,
                column_config={
                    "Section": {"editable": False},
                },
                disabled=["Section"],
            ) 
        save_button = st.form_submit_button("Save")

    if save_button:
        edited_segment_dict = {row["Section"]: row["Content"] for row in edited_segment.to_dict(orient="records")}
        callbacks.set_segment_results(edited_segment_dict)
        save_sucess = st.toast('Saved', icon="💾")
    
def display_parse_results():
    col1, col2 = st.columns(spec=[1, 1], gap="large")

    with col1:
        ui_width = st_javascript("window.innerWidth")
        display_pdf(callbacks.get_resume(), ui_width -10)
    
    with col2:
        with st.container(height=80, border=False):
            st.empty
        callbacks.segment_resume()
        segment_results = callbacks.get_segment_results()
        display_results(segment_results)

        with st.form("job_description_form", border=True):
            st.header("Resume Analysis")
            job_description = st.text_area("Enter the job description of your desired role here.", height=200, key='job_description')
            analyse_btn = st.form_submit_button("Proceed", on_click=callbacks.analyse_job_description, type='primary')
        if analyse_btn:
            st.switch_page('pages/analysis.py')
        

def analysis():
    col1, col2 = st.columns([1,1], gap='large')
    with col1:
        with st.form("job_description_form", border=False):
            st.header("Resume Analysis")
            job_description = st.text_area("Enter the job description of your desired role here.", height=250, key='job_description')
            analyse_btn = st.form_submit_button("Analyse", on_click=callbacks.analyse_job_description, type='primary')
        score = 0
        score_container = st.empty()
        score_container.metric(label="Compatibility Score", value=None)
        if analyse_btn:
            score_container.empty
            score_container.metric(label="Compatibility Score", value=72)
    with col2:
        with st.chat_message("ai"):
            if analyse_btn:
                ## get entities extracted
                ## enter entities into chatbot
                st.write(st.session_state.entities)
            else:
                st.write("Hello 👋 \n Let me help you improve your resume!")

