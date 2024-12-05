import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Initialize session state variables
session_defaults = {
    "query": "",
    "draft": "",
    "txt": "",
    "get_html": "",
    "input_method": "File",
    "uploaded_file": ""
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Function to hide specific page elements
def hide_elements():
    st.markdown("""
    <style>
        .eczjsme18, .st-emotion-cache-1rg1gxd, .st-emotion-cache-1b1gqd1, .st-emotion-cache-4z1n4l, .stAppToolbar {
                display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

hide_elements()

# Page header
st.header("Here you go:")

# Main page rendering function
def render_page():
    """Render the main page and handle navigation."""
    if not st.session_state.get("get_html"):
        st.warning("Please go back to input your assignment")
        return

    st.write(st.session_state.get_html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    if col1.button("Prev", key="advicePrev"):
        switch_page("main")

    # Uncomment if "Next" functionality is needed later
    # if col2.button("Next", key="adviceNext"):
    #     switch_page("More")

# Render the page
render_page()
