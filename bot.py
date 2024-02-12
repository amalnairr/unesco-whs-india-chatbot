import argparse
from dataclasses import dataclass
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st
import warnings

warnings.filterwarnings("ignore")

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Here is some information:

{context}

---------

Answer the question based on the above: {question}
"""


with open("OPENAI_API_KEY.txt", "r") as f:
    OPENAI_API_KEY = f.read().strip()

# creating the vector database (DB) and calling the model 

embedding_function = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY)
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
model = ChatOpenAI(openai_api_key = OPENAI_API_KEY)

def answer_query(query_text):
    
    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=2)
    if len(results) == 0 or results[0][1] < 0.7:
        return(f"Unable to find matching results. Ask another question.")

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    #print(prompt)
    
    response_text = model.predict(prompt)

    #sources = [doc.metadata.get("source", None) for doc, _score in results]
    
    return response_text
    

st.title("Ask me Anything - UNESCO World Heritage Sites in India")
st.markdown("India has 42 UNESCO World Heritage Sites, the sixth most of any country. These sites are recognized for their outstanding universal value and are important for the collective interest of humanity. Ask me anything about these sites and I will try to answer your questions using the information I have learned from the Wikipedia pages of these sites. I have been trained on a dataset of Wikipedia pages of these sites and can answer questions based on the information I have learned. Please note that sometimes I may not be able to answer all questions accurately. Please ask me questions in the format: 'When was the Taj Mahal built?' or 'What is the area of the Sundarbans?' and I will try to answer them to the best of my ability. If I am unable to find matching results, I will let you know. Let's get started..")

st.image("Taj.jpg", use_column_width=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me a Question: When was the Taj Mahal built?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    answer = answer_query(query_text=prompt)
    
    response = f"LiP: {answer}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})