import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import backend
import json
import main

if "query" not in st.session_state:
    st.session_state["query"] = ""
if "draft" not in st.session_state:
    st.session_state["draft"] = ""
if "get_html" not in st.session_state:
    st.session_state["get_html"] = ""

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


def printer():
    print("print===")
    # print(main.get_html)
    print(st.session_state)


def page():
    # with st.spinner('Reviewing...'):
    # response = backend.advice_response(
    #     instruction=main.query_text, answer=main.draft_answer)
    # with open('data.json', 'w', encoding='utf-8') as f:
    #     json.dump(response, f, ensure_ascii=False, indent=4)

    # f = open('data.json')
    # html_text = json.load(f)
    # html_text = html_text.get("text")
    # f.close()
    # st.text_area(
    #     "Area",
    #     on_change=printer,
    #     # on_change=main.aka
    # )
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
