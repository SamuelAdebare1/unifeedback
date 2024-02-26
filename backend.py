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
openai_api_key = os.getenv("OPENAI_API_KEY")


def advice_response(instruction, answer):
    template = """ Assume the role of a university professor and review my assignment. The instruction for the assignment is: "{instruction}" and my answer is: "{answer}". What other things should I add or remove to make the assignment the best it can be? Let your response be in html format. Answer in the same language as it is in the {answer}.
    """
    prompt_template = PromptTemplate(
        input_variables=["instruction", "answer"],
        template=template
    )

    llm = OpenAI(temperature=0.7,
                 api_key=openai_api_key[1:])
    chain = LLMChain(llm=llm, prompt=prompt_template)
    # print(prompt_template)
    return chain.invoke({"instruction": instruction,
                        "answer": answer})


response = advice_response("What is democracy", "It is a form of government")
# response = '{"instruction": "What is democracy", "answer": "Democracy is a form of government system", "text": "Text retrieved"}'
# print(response)
# response = json.loads(f"{response}")

# print(response.get("text"))
print(response)
