"""
this is where you define your pages (as classes with static "loadPage" functions)
and build your pages with the components you created
"""

from src import components
from streamlit_javascript import st_javascript
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
        components.component_say_hello()
        components.component_change_page()
        uploaded_file = components.pdfUploader()
        col1, col2 = st.columns(spec=[2, 1], gap="small")
        if uploaded_file:
            with col1:
                ui_width = st_javascript("window.innerWidth")
                components.displayPDF(uploaded_file, ui_width -10)
            
            with col2:
                st.write("Hello")


        
    def load_pdf_uploader():
        uploaded_file = components.pdfUploader()
        if uploaded_file:
            print(uploaded_file)
            callbacks.set_page_mypage1()
    
        return uploaded_file
    
        
            


# EXAMPLE PAGE ================================================================================
class MyPage1():
    """
    Example Page class
    """
    @staticmethod
    def load_mypage1():
        """
        example page load function
        """
        components.component_say_hello()
        components.component_mypage1_title()
        

    def load_pdf(uploaded_file):
        ui_width = st_javascript("window.innerWidth")
        components.displayPDF(uploaded_file, ui_width)

