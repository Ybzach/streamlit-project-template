"""
this is where you define your pages (as classes with static "loadPage" functions)
and build your pages with the components you created
"""

from src import components
from src import callbacks
import streamlit as st

# HOME PAGE ================================================================================
class HomePage():
    """
    Your Home / Landing Page
    Here you can add your defined components under the loadPage() function
    """
    @staticmethod
    def load_home_page():
        """
        example home page load function
        """
        components.home_title()
        components.pdf_uploader()
        if st.session_state['submitted']:
            st.switch_page('pages/parser.py')

       
class ParserPage():
    """
    Example Page class
    """
    @staticmethod
    def load_page():
        """
        example page load function
        """
        home_button = st.button('Home')
        if home_button:
            callbacks.update_submit(False)
            st.switch_page('app.py')
        components.parser_title()
        components.parser_ui()
        

    def load_pdf(uploaded_file):
        ui_width = st_javascript("window.innerWidth")
        components.displayPDF(uploaded_file, ui_width)

