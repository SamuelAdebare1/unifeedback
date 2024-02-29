from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms import OpenAI
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
# import os

st.title('Docbot')

st.markdown("""
<style>
    .eczjsme11 {
            display: none;
    }  
</style>
""", unsafe_allow_html=True)


def generate_response(uploaded_file, openai_api_key, query_text):
    # Load document if file is uploaded
    if uploaded_file is not None:
        documents = [uploaded_file.read().decode()]
        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.create_documents(documents)
        # Select embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        # Create a vectorstore from documents
        db = Chroma.from_documents(texts, embeddings)
        # Create retriever interface
        retriever = db.as_retriever()
        # Create QA chain
        qa = RetrievalQA.from_chain_type(llm=OpenAI(
            openai_api_key=openai_api_key), chain_type='stuff', retriever=retriever)
        return qa.run(query_text)


# File upload
uploaded_file = st.file_uploader('Upload an article', type='txt')
# Query text
query_text = st.text_input(
    'Enter your question:',
    placeholder='Please provide a short summary.',
    # disabled=not uploaded_file
)

# Form input and query
result = []
# with st.form('myform', clear_on_submit=True):
openai_api_key = st.secrets["OPENAI_API_KEY"]
submitted = st.button(
    'Submit',
    # disabled=not (uploaded_file and query_text)
)
if submitted and openai_api_key.startswith('sk-') and query_text:
    with st.spinner('Calculating...'):
        response = generate_response(
            uploaded_file, openai_api_key, query_text)
        result.append(response)
else:
    st.warning(
        "Please confirm that all inputs are correctly provided before submitting.")

if len(result):
    st.info(response)


def more_page():
    prev = st.button("Prev")
    if prev:
        switch_page("Advice")


more_page()
