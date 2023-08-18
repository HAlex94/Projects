import os
import re
import streamlit as st
import requests
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA


# Set OpenAI API Key
from apikey import API_KEY
os.environ['OPENAI_API_KEY'] = API_KEY

def generate_reponse(drug_info, query):
    # Preprocess the drug_info_text
    drug_info_text = ' '.join([str(value) for value in drug_info.values()])
        
    # 1. Remove HTML tags
    drug_info_text = re.sub(r'<.*?>', ' ', drug_info_text)
    # 2. Remove special characters
    drug_info_text = re.sub(r'[•:;[\]{}]', '', drug_info_text)
    # 3. Replace multiple spaces with a single space
    drug_info_text = re.sub(r'\s+', ' ', drug_info_text).strip()

    # Calculate the maximum allowable tokens for drug_info_text
    buffer_for_completion = 2000  # Setting a buffer for the completion
    max_tokens_for_drug_info = 4097 - len(query.split()) - buffer_for_completion

    # Check token count and truncate if necessary
    if len(drug_info_text.split()) > max_tokens_for_drug_info:
        drug_info_text = ' '.join(drug_info_text.split()[:max_tokens_for_drug_info])

    # Initialize TextSplitter and VectorStore
    text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=500, chunk_overlap=200)
    split_text = text_splitter.split_text(drug_info_text)

    # Embeddings
    db = Chroma.from_texts(split_text, OpenAIEmbeddings())
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 1})
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)

    response = qa.run(query)

    return response



# Streamlit App
st.title('Pharmacy Consultation App')

# User inputs the drug name
drug_name = st.text_input('Enter the drug name:')

if drug_name:
    # Fetch drug information from openFDA API
    response = requests.get(f'https://api.fda.gov/drug/label.json?search={drug_name}&limit=1')
    if response.status_code == 200:
        drug_info = response.json()['results'][0]

        # Display drug summary
        #st.subheader('Drug Summary')
        #st.write(drug_info)

        # Consultation section
        st.subheader('Consultation')
        scenarios = ['Missed a dose', 'Takes double the dose']
        for scenario in scenarios:
            question = f'What to do if a patient {scenario} of {drug_name}?'
            response = generate_reponse(drug_info, question)
            st.write(f'**{scenario}**: {response}')

        # Chatbot interface
        st.subheader('Chatbot')
        question = st.text_input('Ask a question:')
        if question:
            response = generate_reponse(drug_info, question)
            st.write(response)
    else:
        st.write('Error fetching drug information. Please try again.')
