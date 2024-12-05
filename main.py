import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import backend
import json
import pdfplumber
import docx2txt

# Initialize session state
def initialize_session_state():
    defaults = {
        "query": "",
        "get_html": "",
        "the_question": "",
        "uploaded_file": None,
        "file_content": "",
        "the_text": ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# Utility functions
def read_text_from_txt(file_contents):
    return file_contents.decode("utf-8")

def read_text_from_pdf(pdf_io):
    try:
        data = ""
        with pdfplumber.open(pdf_io) as pdf:
            for page in pdf.pages:
                data += page.extract_text()
        return data
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return ""

def professor(question, answer):
    """
    Processes the assignment question and answer using the backend and saves the output.

    Args:
        question (str): Assignment question.
        answer (str): Drafted answer.

    Returns:
        str: HTML response from the backend.
    """
    with st.spinner('Reviewing...'):
        try:
            response = backend.advice_response(instruction=question, answer=answer)
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(response, f, ensure_ascii=False, indent=4)
            with open('data.json') as f:
                html_text = json.load(f).get("text")
            return html_text
        except Exception as e:
            st.error(f"Error processing input: {e}")
            return ""

@st.cache_data
def process_uploaded_file(file):
    """
    Extracts text from the uploaded file.

    Args:
        file: Uploaded file object.

    Returns:
        str: Extracted text.
    """
    if file.type == "text/plain":
        return read_text_from_txt(file.read())
    elif file.type == "application/pdf":
        return read_text_from_pdf(file)
    elif file.name.lower().endswith(".docx"):
        return docx2txt.process(file)
    else:
        raise ValueError("Unsupported file format")

# UI Components
st.title('Your One-Stop Assignment Hub')

# Removing some Streamlit elements on the page via CSS

st.markdown("""
    <style>
        .eczjsme18, .st-emotion-cache-1rg1gxd, .st-emotion-cache-1b1gqd1, .st-emotion-cache-4z1n4l, .stAppToolbar {
                display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Text Input for Assignment Question
def update_query_text():
    st.session_state.the_question = st.session_state.assignment_question

query_text = st.text_area(
    "Enter the assignment's question:",
    key="assignment_question",
    placeholder="Please input the assignment's instruction",
    value=st.session_state.the_question,
    on_change=update_query_text,
    help="Provide clear instructions or questions for your assignment."
)

# Tabs for File Upload and Text Input
tab1, tab2 = st.tabs(["File Upload", "Text Input"])

with tab1:
    st.header("Upload your assignment")
    uploaded_file = st.file_uploader('Upload your draft file', type=['txt', 'pdf', 'docx'])

    if uploaded_file is not None:
        try:
            st.session_state.file_content = process_uploaded_file(uploaded_file)
            st.success("File successfully uploaded and processed!")
        except ValueError as e:
            st.warning(str(e))

        if st.button("Submit file for Review", key="tab1"):
            if query_text:
                st.session_state.get_html = professor(
                    st.session_state.the_question, st.session_state.file_content
                )
                switch_page("Advice")
            else:
                st.warning("All input fields must be filled.")

with tab2:
    st.header("Paste your assignment text")

    def update_draft_answer_text():
        st.session_state.the_text = st.session_state.draft_answer_key

    draft_answer = st.text_area(
        'Enter your drafted answer:',
        key="draft_answer_key",
        height=300,
        placeholder="Please input your answer",
        value=st.session_state.the_text,
        on_change=update_draft_answer_text,
        help="Paste your answer or write it directly here."
    )

    if st.button("Submit text for Review", key="tab2"):
        if query_text:
            st.session_state.get_html = professor(
                st.session_state.the_question, st.session_state.the_text
            )
            switch_page("Advice")
        else:
            st.warning("All input fields must be filled.")
