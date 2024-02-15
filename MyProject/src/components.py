"""
this is where you define your components
every component is a piece of row of your application
"""

import streamlit as st
from src import callbacks
import base64

def component_say_hello():
    """
    example component with a home button and header
    """
    st.button('Home', on_click=callbacks.set_page_home)
    st.header('Hello World!')


def component_change_page():
    """
    example component with a page selection
    """
    st.write('Where do you want to go?')
    st.button('Page 1', on_click=callbacks.set_page_mypage1)
    st.button('Page 2', on_click=callbacks.set_page_mypage2)


def component_mypage1_title():
    """
    example component with mypage1 page info
    """
    st.write('My Page 1')


def displayPDF(upl_file, width):
    # Read file as bytes:
    bytes_data = upl_file.getvalue()

    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode("utf-8", 'ignore')

    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str(width)} height={str(width*4/3)} type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)

def pdfUploader():
    uploaded_file = st.file_uploader(
        "Upload file",
        type=["pdf"],
        help="Only PDF files are supported",
        # on_change=clear_submit,
    )

    return uploaded_file
