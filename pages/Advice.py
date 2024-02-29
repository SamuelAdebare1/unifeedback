import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import backend
import json
import main

if "query" not in st.session_state:
    st.session_state["query"] = ""
if "draft" not in st.session_state:
    st.session_state["draft"] = ""
if "file_content" not in st.session_state:
    st.session_state["txt"] = ""
if "get_html" not in st.session_state:
    st.session_state["get_html"] = ""
if "input_method" not in st.session_state:
    st.session_state["input_method"] = "File"
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = ""


st.markdown("""
<style>
    .eczjsme11 {
            display: none;
    }  
    # .e1f1d6gn3 .e1f1d6gn0 {
    #         text-align:right;
    # }
</style>
""", unsafe_allow_html=True)


def page():
    st.write(
        st.session_state.get_html,
        unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    prev = col1.button("Prev", key="advicePrev")
    nextt = col2.button("Next", key="adviceNext")

    if prev:
        switch_page("main")
    elif nextt:
        switch_page("More")


page()
if st.session_state.get_html == "":
    st.warning("Please go back to input your assigment")
