# importing required modules
import pdfplumber
from pypdf import PdfReader

# # creating a pdf reader object
# reader = PdfReader('Samuel O.pdf')

# # printing number of pages in pdf file
# print(len(reader.pages))

# # getting a specific page from the pdf file
# page = reader.pages[0]

# # extracting text from page
# text = page.extract_text()
# print(text)


def extract_data(pdf_io):
    data = ""
    with pdfplumber.open(pdf_io) as pdf:
        pages = pdf.pages
        for p in pages:
            # data.append(p.extract_text())
            data += p.extract_text()
    return data


print(extract_data("Samuel O.pdf"))
