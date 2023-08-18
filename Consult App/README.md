# Pharmacy Consultation App: A Drug Information Retrieval System

## Introduction:
The Pharmacy Consultation App is a specialized tool designed to facilitate the retrieval of drug-related information. Recognizing the increasing need for quick and accurate access to pharmaceutical data, this application serves as a bridge between the vast datasets available and the specific queries of users, be they healthcare professionals, researchers, or the general public. The scope of this project encompasses real-time data retrieval, advanced natural language processing, and an intuitive user interface.

## Methodology:

- **Data Retrieval and Preprocessing:** The application is integrated with the openFDA API, a comprehensive drug database provided by the U.S. Food and Drug Administration (FDA). Upon receiving a drug name as input, the system fetches relevant drug information. This data is then preprocessed to remove extraneous elements such as HTML tags and special characters, ensuring its readiness for NLP tasks.

- **Natural Language Processing (NLP):** At its core, the application utilizes a sophisticated NLP model to interpret and respond to user queries. This model is adept at understanding a wide range of query phrasings and generating contextually relevant responses.

- **Text Splitting and Embeddings:** Due to token limitations inherent to many NLP models, the application employs a CharacterTextSplitter to divide the preprocessed drug information into manageable segments. These segments are subsequently embedded using the OpenAIEmbeddings technique, enabling efficient text retrieval.

- **Retrieval-Based Question Answering:** The embedded text segments are stored within a Chroma vector store. When a user submits a query, the application deploys a retrieval-based QA system. This system identifies the most pertinent text segment from the vector store and then leverages the NLP model to craft a concise, relevant response.

## User Interface:
The application's interface, developed using Streamlit, is designed for ease of use. Users can effortlessly input drug names, view a summarized drug profile, and pose specific questions. Additionally, the interface offers predefined scenarios such as "missed a dose" or "double dosing", providing rapid answers to frequently asked questions.

## Limitations:

1. **Data Source Dependency:** The application's accuracy and reliability are contingent upon the openFDA API's data quality and availability.
2. **Token Limitation:** The NLP model has inherent token constraints, which may necessitate truncation of extensive drug information, potentially omitting vital details.
3. **Static Scenarios:** While the app offers predefined scenarios, it may not cover all possible drug-related queries.
4. **Complex Queries:** The system is optimized for standard questions, and intricate queries might receive less detailed answers.
5. **Language and Terminology:** The application is primarily tailored for English queries and might not always recognize specialized pharmaceutical terms.

## Installation:
### Prerequisites:
- Python 3.7 or higher
- An OpenAI API key
- Code Editor (can also run in a Google Colab or Jupyter Notebook)
  
To set up the Pharmacy Consultation App on your local machine:

1. **Clone the Repository:** 
   ```bash
   git clone https://github.com/HAlex94/Projects/tree/main/Consult%20App

2. **Go to the Folder Directory**
   ```bash
   cd Consult App  
3. **Install Dependencies**
    ```bash
    pip install streamlit openai langchain chromadb 
    ```
4. **Set Up OpenAI API Key**:
 Open the apikey.py file and add your OpenAI API

5. **Run Streamlit**:
    ```bash
      streamlit run pharmacy_app.py
    ```

## Example
![Screenshot 2023-08-18 104429](https://github.com/HAlex94/Projects/assets/108144585/01f2f9c8-ac1e-44f3-b106-39fb42a1fa7d)
