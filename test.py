# import streamlit as st
# from pypdf import PdfReader  # for PDF files
# import pdfplumber
# from streamlit_extras.switch_page_button import switch_page


# def read_text_from_txt(file_contents):
#     return file_contents.decode("utf-8")


# def read_text_from_pdf(pdf_io):
#     data = ""
#     with pdfplumber.open(pdf_io) as pdf:
#         pages = pdf.pages
#         for p in pages:
#             data += p.extract_text()
#     return data


# def extractor(uploaded):
#     if uploaded is not None:
#         file_contents = uploaded.read()

#         st.write("### Displaying the content of the uploaded file:")

#         if uploaded.type == "text/plain":
#             # For text files (txt)
#             text_result = read_text_from_txt(file_contents)
#             st.text(text_result)
#         elif uploaded.type == "application/pdf":
#             # For PDF files
#             # df = extract_data(uploaded)
#             text_result = read_text_from_pdf(uploaded)
#             st.text(text_result)
#         else:
#             st.warning(
#                 "Unsupported file format. Please upload a .txt or .pdf file.")


# def main():
#     st.title("File Uploader and Text Extractor")

#     uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf"])
#     extractor(uploaded_file)


# if __name__ == "__main__":
#     main()
