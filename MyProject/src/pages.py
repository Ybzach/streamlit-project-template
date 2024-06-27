"""
this is where you define your pages (as classes with static "loadPage" functions)
and build your pages with the components you created
"""

from src import components
from src import callbacks
import streamlit as st
from langchain_core.messages import AIMessage

# HOME PAGE ================================================================================
class HomePage():
    @staticmethod
    def load_home_page():
        components.home_title()
        components.pdf_uploader()
        if st.session_state['submitted']:
            st.switch_page('pages/parser.py')

class ParserPage():
    @staticmethod
    def load_page():
        # components.parser_title()
        components.display_parse_results()

class ChatPage():
    @staticmethod
    def load_page():
        col1, col2, col3 = st.columns([1, 8, 2])
        with col1:
            segment_btn = st.button('Return')
        with col3:
            home_button = st.button('Upload another resume', type='primary', use_container_width=True)
        if home_button:
            st.switch_page('app.py')
        if segment_btn:
            st.switch_page('pages/parser.py')
        components.chat()
        if st.session_state['initial_analysis'] == "":
            callbacks.analyse_job_description()
            intial_analysis = st.chat_message("assistant").write_stream(components.generate_prompt())
            st.session_state['initial_analysis'] = intial_analysis
            st.session_state.messages.append(AIMessage(content=intial_analysis))

