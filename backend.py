from dotenv import load_dotenv
import os
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from streamlit_extras.switch_page_button import switch_page
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain
import json


load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_key = st.secrets["OPENAI_API_KEY"]


def advice_response(instruction, answer):
    template = """ Assume the role of a university professor and review my assignment. I am a university student and you are addressing me only so don't say things like "Welcome to our class!". The instruction for the assignment is: "{instruction}" and my answer is: "{answer}". What other things should I add or remove to make the assignment the best it can be? Your response MUST be in html body format. Response containing pretty HTML that includes <li>, <italics>, <bold> etc is considered good. Answer in the same language as it is in the {answer}.
    """
    prompt_template = PromptTemplate(
        input_variables=["instruction", "answer"],
        template=template
    )

    llm = OpenAI(temperature=0.95,
                 api_key=openai_api_key,
                 #  max_tokens=4094
                 )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain.invoke({"instruction": instruction, "answer": answer})
