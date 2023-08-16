import streamlit as st
import openai
import pandas as pd
import os
from PyPDF2 import PdfReader

# Set OpenAI API Key
from apikey import API_KEY
os.environ['OPENAI_API_KEY'] = API_KEY

def pdf_to_text(file):
    """
    Extract text from a PDF file.
    """
    pdf = PdfReader(file)
    return ''.join(page.extract_text() for page in pdf.pages)

def split_text(text, max_tokens=1000):
    """
    Split text into chunks, each with a maximum number of tokens.
    """
    tokens = text.split()
    text_chunks = []
    current_chunk = []
    current_chunk_tokens = 0

    for token in tokens:
        token_length = len(token)

        if current_chunk_tokens + token_length > max_tokens:
            text_chunks.append(" ".join(current_chunk))
            current_chunk = [token]
            current_chunk_tokens = token_length
        else:
            current_chunk.append(token)
            current_chunk_tokens += token_length

    if current_chunk:
        text_chunks.append(" ".join(current_chunk))

    return text_chunks

def generate_summary(prompt, text):
    """
    Generate a concise summary for the given text using OpenAI's gpt-3.5-turbo model.
    """
    text_chunks = split_text(text)
    summary_chunks = []

    for chunk in text_chunks:
        # Use the chat-based interface for gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."},
                {"role": "user", "content": f"{prompt}: {chunk}"}
            ]
        )
        # Extract the assistant's reply from the response
        summary_chunks.append(response['choices'][0]['message']['content'].strip())

    # Further summarize the combined summaries
    combined_summary = ' '.join(summary_chunks)[:3000]  # Ensure it doesn't exceed model's token limit
    final_summary_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."},
            {"role": "user", "content": f"{prompt}: {combined_summary}"}
        ]
    )

    return final_summary_response['choices'][0]['message']['content'].strip()

def ask_question(context, question):
    """
    Use the gpt-3.5-turbo model to answer a question based on the provided context.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following context and answer any questions prompted by the user. Please avoid unnecessary details or tangential points."},
            {"role": "user", "content": context},
            {"role": "user", "content": question}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Streamlit configurations
st.set_page_config(page_title="Scientific Article & CSV Data Summarizer", page_icon=":books:", layout="centered")
st.title("Scientific Article & CSV Data Summarizer")

input_type = st.selectbox("Choose input type", ("PDF", "CSV"))

if input_type == "PDF":
    uploaded_file = st.file_uploader("Upload a PDF scientific article", type=["pdf"])

    if uploaded_file:
        with st.spinner("Extracting text from PDF..."):
            article_text = pdf_to_text(uploaded_file)

        # Chatbot feature
        user_question = st.text_input("Ask a question about the uploaded document:")
        if user_question:
            with st.spinner("Answering your question..."):
                answer = ask_question(article_text, user_question)
            st.write(f"Answer: {answer}")

        custom_prompt = st.text_input(
            "Enter your custom prompt for summarizing the article",
            "Summarize the main points of this article. Keep your summary to less than 300 words. Use a mix of paragraph and bullet point formating for your response."
        )

        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                summary = generate_summary(custom_prompt, article_text)
            st.write(summary)

elif input_type == "CSV":
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file:
        with st.spinner("Reading CSV data..."):
            data = pd.read_csv(uploaded_file)
            st.write("CSV Data:")
            st.dataframe(data)

        custom_prompt = st.text_input(
            "Enter your custom prompt for interpreting the CSV data",
            "Summarize the main insights from the data"
        )

        if st.button("Interpret Data"):
            with st.spinner("Interpreting data..."):
                interpretation = generate_summary(custom_prompt, data.to_string())
            st.write(interpretation)