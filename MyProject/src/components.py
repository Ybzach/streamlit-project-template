"""
this is where you define your components
every component is a piece of row of your application
"""

import streamlit as st
from src import callbacks
from streamlit_javascript import st_javascript
import pandas as pd
import base64
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


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

        st.header("Resume Analysis")
        job_description = st.text_area("Enter the job description of your desired role here.", height=200)
        if job_description:
            callbacks.save_job_description(job_description)

        openai_api_key = st.text_input(
            "Insert your OpenAI API Key to generate feedback on your resume", 
            # key="openai_api_key",
            type='password',
            placeholder="Paste your OpenAI API Key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys."
        )
        if openai_api_key:
            callbacks.set_openai_api_key(openai_api_key)

        analyse_btn = st.button("Generate feedback")
        if analyse_btn:
            st.session_state['initial_analysis'] = ""
            st.session_state.messages = []
            st.switch_page('pages/chat.py')

def remove_duplicates(lst):
    if not lst:
        return []
    return list(set(lst))

def generate_prompt():
    template = """
        You are a resume reviewer. Remember, you are the reviewer.
        You have been asked to review a resume for their compatibility with a job description by these categories: [experience, education, required skills]]
        You will be given the keywords from the job description of each category and the section in the resume that corresponds to each category in the following format:

        Exprience keywords: {exprience_keywords}

        Exprience section: {exprience_section}
        
        Education keywords: {education_keywords}

        Education section: {education_section}

        Required Skills keywords: {required_skills_keywords}

        Required Skills section: {required_skills_section}

        There is a possibility that you will receive an empty keyword list or resume section. In that case, you can acknowledge that the section is empty, and that you can't provide any feedback on that section.
        Here are some additional information from the resume that you can use to evaluate the candidate:

        Extracurricular Activities/Volunteer Experience: {involvements_section}
        
        Projects: {projects_section}
        
        Based on the keywords and sections provided, review the resume about the candidate's compatibility with the job description, based on each category.
        Write the review by using a paragraph for each category, with the category name as the header.
        After reviewing the all the sections, provide a bullet list of actionable items to the user on how they can improve the resume to better match the job description.
    """
    jd_entities = st.session_state['entities']
    resume_sections = st.session_state['segment_results']
    llm = ChatOpenAI(openai_api_key=st.session_state['openai_api_key'], model_name="gpt-3.5-turbo")
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "exprience_keywords": remove_duplicates(jd_entities.get('EXP', [])),
        "exprience_section": resume_sections.get('EXPERIENCE', []),
        "education_keywords": remove_duplicates(jd_entities.get('EDU', [])),
        "education_section": resume_sections.get('EDUCATION', []),
        "required_skills_keywords": remove_duplicates(jd_entities.get('REQUIRED-S', [])),
        "required_skills_section": resume_sections.get('SKILL', []),
        "involvements_section": resume_sections.get('INVOLVEMENTS', []),
        "projects_section": resume_sections.get('PROJECT', [])
    })

    # return prompt_query

def get_response(user_query, chat_history):

    template = """
    You are a helpful assistant that helps review and improve the compatibility between a resume and a job description. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(openai_api_key=st.session_state['openai_api_key'], model_name="gpt-3.5-turbo")
        
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })


def chat():
    for message in st.session_state.messages:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

    if prompt := st.chat_input(placeholder="What skills am I lacking?"):
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("Human"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.write_stream(get_response(prompt, st.session_state.messages))
        st.session_state.messages.append(AIMessage(content=response))
