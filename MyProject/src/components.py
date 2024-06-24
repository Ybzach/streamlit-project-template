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

lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus interdum, metus a pharetra rhoncus, elit neque ornare eros, at sodales felis nibh nec tortor. Maecenas diam arcu, dignissim ut dignissim id, eleifend ac felis. Quisque a sollicitudin ipsum. Suspendisse tempus at tortor sit amet fringilla. Nullam augue ligula, condimentum eu elementum vel, mollis non erat. Mauris libero sem, imperdiet eget nulla et, tincidunt sodales enim. Nam interdum tincidunt metus, at euismod augue facilisis ac. Vestibulum ornare orci sit amet massa viverra aliquam. Ut sodales vitae turpis in vestibulum. Nam rutrum fringilla neque ut semper. Morbi non imperdiet sapien. Duis quis turpis et eros consectetur sollicitudin ac ac sapien. Mauris ligula orci, euismod in varius at, sodales nec mauris. Donec posuere lacus dui, dictum mollis odio sodales nec.\nVivamus nulla tellus, feugiat ac mauris ut, egestas sodales urna. Ut faucibus rutrum dapibus. Duis pulvinar vitae massa sit amet pellentesque. Etiam non arcu vel mauris auctor placerat. Pellentesque id quam tempor, malesuada diam eu, laoreet ante. Nullam nec mi porttitor, sagittis augue vitae, rhoncus neque. Nulla tempus venenatis nisi. Maecenas porttitor fermentum mollis. Aliquam dapibus tellus non imperdiet molestie. Praesent dictum odio ut mauris molestie, et dictum massa viverra. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Donec et consequat dolor, ac sagittis felis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Interdum et malesuada fames ac ante ipsum primis in faucibus. '

def home_button():
    """
    home button 
    """
    st.button('Home')

def home_title():
    """
    example component with mypage1 page info
    """
    st.title('End-to-End Resume Analysis with LLM :brain:')

def parser_title():
    """
    example component with mypage1 page info
    """
    st.title('Resume Analysis')


def display_pdf(upl_file, width):
    # Read file as bytes:
    bytes_data = upl_file.getvalue()

    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode("utf-8", 'ignore')

    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str(width)} height={str(width*4/3)} type="application/pdf"></iframe>'

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

def parser_ui():
    tab1, tab2 = st.tabs(["Parser", "Analysis"])
    with tab1:
        display_parse_results()
    with tab2:
        analysis()

def parser_results():
    # df = pd.DataFrame(
    # {
    #     "feature": ["University", "Degree", "CGPA", 'Graduation Date'],
    #     "results": ["XYZ University", "Bachelor of Science in Computer Science", "3.8", "May 2023"],
    # }
    # )

    # st.dataframe(
    #     df,
    #     column_config={
    #         "feature": st.column_config.TextColumn(
    #             "Entity",
    #         ),
    #         "results": st.column_config.TextColumn(
    #             "Extracted Text",
    #         ),
    #     },
    #     hide_index=True,
    # )

    st.dataframe(callbacks.get_segment())

def display_parse_results():
    col1, col2 = st.columns(spec=[1, 1], gap="large")
    resume = callbacks.get_resume()
    # if st.session_state['submitted']:
    #     parse_status = st.toast('Resume uploaded successfully', icon="🎉")
    with col1:
        ui_width = st_javascript("window.innerWidth")
        display_pdf(resume, ui_width -10)
    
    with col2:
        with st.spinner('Parsing Resume...'):
            callbacks.segment_resume(resume)
        parser_results()
        st.button("Update")


def analysis():
    col1, col2 = st.columns([1,1], gap='large')
    
    with col1:
        job_description = st.text_area("Insert Job Description Here", height=250)
        calculate_btn = st.button("Calculate", on_click=output_analysis)
        score = 0
        score_container = st.empty()
        score_container.metric(label="Compatibility Score", value=None)
        if calculate_btn:
            score_container.empty
            score_container.metric(label="Compatibility Score", value=72)
    with col2:
        with st.chat_message("ai"):
            if calculate_btn:
                st.write(lorem)
            else:
                st.write("Hello 👋 \n Let me help you improve your resume!")
        
        

def output_analysis():
    st.session_state['analysis'] = 'output'
