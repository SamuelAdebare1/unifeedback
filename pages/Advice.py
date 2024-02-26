import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import backend


st.title('Advice')

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
    # st.text_area("Sugestions", height=500)
    html = """
            <h1>You should do this</h1>
            <h1>You should remove this</h1>
        """
    st.write(
        html,
        unsafe_allow_html=True)
    # html = st.markdown("""<h1>You should do this</h1>""",
    #                    unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    prev = col1.button("Prev")
    nextt = col2.button("Next")

    if prev:
        switch_page("main")
    elif nextt:
        switch_page("More")


page()
