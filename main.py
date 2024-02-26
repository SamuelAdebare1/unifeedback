import streamlit as st
from streamlit_extras.switch_page_button import switch_page


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


def printer(x):
    # st.session_state.query
    print(x)


# Query text
query_text = st.text_area(
    'Enter the question:',
    placeholder='Please input the assignment\'s instruction',
    value=st.session_state.query,
    # on_change=printer,
    # args=(query_text,)
)
# Query text
draft_answer = st.text_area(
    'Enter your drafted answer:',
    height=300,
    placeholder='Please input your answer',
    value=st.session_state.draft)

# Form input and query
# result = []
# with st.form('myform', clear_on_submit=True):
#     solution = st.text_area('Assignment',
#                             placeholder="Paste your draft",)
#     submitted = st.form_submit_button(
#         'Submit')
#     if submitted:
#         with st.spinner('Calculating...'):
#             st.write("Hello")


def session_update():
    st.session_state.query = query_text


def main_page():
    next = st.button("Next", disabled=not (query_text and draft_answer))
    if next:

        # set the value to session
        st.session_state.query = query_text
        st.session_state.draft = draft_answer
        # Get or print the two inputs
        # print(st.session_state.query)
        # print(st.session_state.draft)
        switch_page("Advice")


main_page()
