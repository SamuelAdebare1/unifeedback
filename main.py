import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import backend
import json
# import time
import pdfplumber
# import textract
# import codecs
# import os
import docx2txt


def read_text_from_txt(file_contents):
    return file_contents.decode("utf-8")


def read_text_from_pdf(pdf_io):
    data = ""
    with pdfplumber.open(pdf_io) as pdf:
        pages = pdf.pages
        for p in pages:
            data += p.extract_text()
    return data


st.title('Your one-stop assignment hub')

st.markdown("""
<style>
    .eczjsme11 {
            display: none;
    }  

</style>
""", unsafe_allow_html=True)

if "query" not in st.session_state:
    st.session_state["query"] = ""
if "draft" not in st.session_state:
    st.session_state["draft"] = ""
if "file_content" not in st.session_state:
    st.session_state["txt"] = ""
if "get_html" not in st.session_state:
    st.session_state["get_html"] = ""
if "input_method" not in st.session_state:
    st.session_state["input_method"] = None
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None


# Query text
query_text = st.text_area(
    'Enter the question:',
    placeholder='Please input the assignment\'s instruction',
    value=st.session_state.query,
)
radio_options = ["File", "Text box"]
radio_val = st.radio("Select input method:",
                     radio_options,
                     horizontal=True,
                     key="radio_buttons",
                     index=radio_options.index(st.session_state.input_method or "File"), format_func=lambda x: x
                     #  on_change=radio_switch
                     )
st.session_state["input_method"] = radio_val
# print(radio_val)


# if st.session_state.uploaded_file:
#     print("not empty file")
#     uploaded_file = st.session_state.uploaded_file
# Query answer
if st.session_state["input_method"] == "File":
    uploaded_file = st.file_uploader(
        'Upload your draft', type=['txt', 'pdf', 'docx'])
    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        st.session_state.uploaded_file == uploaded_file
        if uploaded_file.type == "text/plain":
            # For text files (txt)
            text_result = read_text_from_txt(file_contents)
            # st.text(text_result)
            st.session_state.file_content = text_result
        elif uploaded_file.type == "application/pdf":
            # For PDF files
            text_result = read_text_from_pdf(uploaded_file)
            # st.text(text_result)
            st.session_state.file_content = text_result
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or uploaded_file.name.lower().endswith(".docx"):
            # open a named temporary file

            # text = textract.process(uploaded_file.read())
            # decoded_string = codecs.escape_decode(
            #     bytes(f"{text}", "utf-8"))[0].decode("utf-8")

            # text_result = decoded_string
            text_result = docx2txt.process(uploaded_file)
            st.session_state.file_content = text_result
        else:
            st.warning(
                "Unsupported file format. Please upload a .txt, .docx or .pdf file.")

elif st.session_state["input_method"] == "Text box":
    # create on_change to update
    draft_answer = st.text_area(
        'Enter your drafted answer:',
        height=300,
        placeholder='Please input your answer',
        value=st.session_state.draft)


def session_update():
    st.session_state.query = query_text


def generator():
    with st.spinner('Reviewing...'):
        if st.session_state["input_method"] == "Text box":

            response = backend.advice_response(
                instruction=query_text, answer=draft_answer)
        elif st.session_state["input_method"] == "File":
            response = backend.advice_response(
                instruction=query_text, answer=st.session_state.file_content)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=4)
        f = open('data.json')
        html_text = json.load(f)
        html_text = html_text.get("text")
        f.close()
        return html_text


def main_page():
    next = st.button("Submit for Review")
    # radio_val = st.session_state["input_method"]
    if next:
        # if query_text and (draft_answer or uploaded_file):
        if query_text:
            st.session_state.query = query_text
            st.session_state.get_html = generator()
            if st.session_state.input_method == "File":
                # print(uploaded_file)
                # st.session_state.uploaded_file == uploaded_file
                pass
            elif st.session_state.input_method == "Text box":
                st.session_state.draft = draft_answer
            switch_page("Advice")
        else:
            st.warning("All input field must be filled")


main_page()
