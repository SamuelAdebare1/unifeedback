# from langchain.chains import RetrievalQA
# from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_openai import OpenAI
# import streamlit as st
# from streamlit_extras.switch_page_button import switch_page
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms import OpenAI
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from langchain_community.vectorstores import FAISS
import os
import pdfplumber
import docx2txt

# from langchain_community.embeddings import OpenAIEmbeddings

# if "input_method_" not in st.session_state:
#     st.session_state["input_method_"] = "File"
# if "query_" not in st.session_state:
#     st.session_state["query_"] = ""
# if "text_box" not in st.session_state:
#     st.session_state["text_box"] = ""
# if "file_content_" not in st.session_state:
#     st.session_state.file_content_ = ""


def read_text_from_txt(file_contents):
    return file_contents.decode("utf-8")


def read_text_from_pdf(pdf_io):
    data = ""
    with pdfplumber.open(pdf_io) as pdf:
        pages = pdf.pages
        for p in pages:
            data += p.extract_text()
    return data


st.title('Docbot')

st.markdown("""
<style>
    .eczjsme11 {
            display: none;
    }  
</style>
""", unsafe_allow_html=True)


# radio_options = ["File", "Text box"]
# radio_val = st.radio("Select input method:",
#                      radio_options,
#                      horizontal=True,
#                      key="radio_buttons_",
#                      #  index=radio_options.index(st.session_state.input_method_ or "File"),
#                      #  format_func=lambda x: x
#                      #  on_change=radio_switch
#                      )
# st.session_state["input_method_"] = radio_val

# if st.session_state["input_method_"] == "Text box":
#     draft_answer = st.text_area(
#         'Enter your drafted answer:',
#         height=300,
#         placeholder='Please input your answer',
#         # value=st.session_state.text_box
#     )

# elif st.session_state["input_method_"] == "File":
#     # File upload
#     uploaded_file = st.file_uploader(
#         'Upload an article', type=['txt', 'pdf', 'docx'])

# # Query text
# query_text = st.text_input(
#     'Enter your question:',
#     placeholder='Please input yout text',
#     # value=st.session_state["query_"]
#     # disabled=not uploaded_file
# )


def generate_response(uploaded_file, openai_api_key, query_text):
    # Load document if file is uploaded
    if uploaded_file is not None:
        # documents = [uploaded_file.read().decode()]
        # st.write(documents)

        file_contents = uploaded_file.read()
        if uploaded_file.type == "text/plain":
            text_result = read_text_from_txt(file_contents)
            # st.session_state.file_content_ = text_result
        elif uploaded_file.type == "application/pdf":
            text_result = read_text_from_pdf(uploaded_file)
            # st.session_state.file_content_ = text_result
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or uploaded_file.name.lower().endswith(".docx"):
            # text = textract.process(uploaded_file.read())
            # decoded_string = codecs.escape_decode(
            #     bytes(f"{text}", "utf-8"))[0].decode("utf-8")

            # text_result = decoded_string
            text_result = docx2txt.process(uploaded_file)
            # st.session_state.file_content_ = text_result
        else:
            st.warning(
                "Unsupported file format. Please upload a .txt, .docx or .pdf file.")

        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        # documents = st.session_state.file_content_
        documents = text_result
        texts = text_splitter.create_documents(documents)
        # Select embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        # Create a vectorstore from documents
        # db = Chroma.from_documents(texts, embeddings)
        db = FAISS.from_documents(texts, embeddings)
        # Create retriever interface
        retriever = db.as_retriever()
        # Create QA chain
        qa = RetrievalQA.from_chain_type(llm=OpenAI(
            openai_api_key=openai_api_key), chain_type='stuff', retriever=retriever)
        return qa.run(query_text)


# Form input and query
result = []
with st.form('myform', clear_on_submit=True):
    # if st.session_state["input_method_"] == "Text box":
    #     draft_answer = st.text_area(
    #         'Enter your drafted answer:',
    #         height=300,
    #         placeholder='Please input your answer',
    #         # value=st.session_state.text_box
    #     )

    # st.session_state["input_method_"] == "File":
    uploaded_file = st.file_uploader(
        'Upload an article', type=['txt', 'pdf', 'docx'])

    # Query text
    query_text = st.text_input(
        'Enter your question:',
        placeholder='Please input yout text',
        # value=st.session_state["query_"]
        # disabled=not uploaded_file
    )
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    submitted = st.form_submit_button(
        'Submit',
        # disabled=not (uploaded_file and query_text)
    )
    if submitted and openai_api_key.startswith('sk-') and query_text:
        with st.spinner('Calculating...'):
            # st.session_state["query_"] = query_text

            response = generate_response(
                uploaded_file, openai_api_key, query_text)
            # st.session_state.file_content_ =
            result.append(response)
    else:
        st.warning(
            "Please confirm that all inputs are correctly provided before submitting.")

    if len(result):
        st.info(response)


# def more_page():
#     prev = st.button("Prev")
#     if prev:
#         switch_page("Advice")


# more_page()
