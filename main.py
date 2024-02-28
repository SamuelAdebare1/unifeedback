import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import backend
import json
import time


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
if "get_html" not in st.session_state:
    st.session_state["get_html"] = ""


def printer(x):
    # st.session_state.query
    print(x)


# Query text
query_text = st.text_area(
    'Enter the question:',
    placeholder='Please input the assignment\'s instruction',
    value=st.session_state.query,
)
# Query answer
draft_answer = st.text_area(
    'Enter your drafted answer:',
    height=300,
    placeholder='Please input your answer',
    value=st.session_state.draft)


def session_update():
    st.session_state.query = query_text


def generator():
    with st.spinner('Reviewing...'):
        response = backend.advice_response(
            instruction=query_text, answer=draft_answer)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=4)
        f = open('data.json')
        html_text = json.load(f)
        html_text = html_text.get("text")
        f.close()
        return html_text


def main_page():
    next = st.button("Submit for Review")
    if next:
        if query_text and draft_answer:
            st.session_state.query = query_text
            st.session_state.draft = draft_answer
            st.session_state.get_html = generator()
            switch_page("Advice")
        else:
            st.warning("All input field must be filled")


main_page()
