# CBA Contract Copilot – Contract Analysis Chatbot

**Live App:**  
https://contract-analysis-chatbot-zfscsugtdoyvvefq9ypspd.streamlit.app/

---

## Overview

CBA Contract Copilot is an AI-powered chatbot designed to analyze **Collective Bargaining Agreements (CBA)** and other contract documents. The system allows users to upload contract PDFs and ask questions in natural language.

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant clauses from uploaded documents and generate contextual responses using a large language model.

Built using **Streamlit, LangChain, FAISS, and OpenAI GPT models**, the system enables users to quickly extract insights from large contract documents without manually searching through hundreds of pages.

---

## Live Demo

Try the deployed application here:

https://contract-analysis-chatbot-zfscsugtdoyvvefq9ypspd.streamlit.app/

---

## Features

- Upload contract PDF documents
- Semantic search using FAISS vector database
- Retrieval of relevant contract clauses
- LLM-powered question answering
- Interactive chat interface built with Streamlit
- Displays source references including document name and page number
- Handles structured pay-rate tables and contract data
- Context-aware responses using chat history

---

## How It Works

1. Users upload contract PDF files through the Streamlit interface.
2. The system extracts text from the documents.
3. Text is split into smaller chunks.
4. Each chunk is converted into embeddings.
5. Embeddings are stored in a FAISS vector database.
6. When a question is asked, the system retrieves the most relevant document chunks.
7. The retrieved context is passed to an OpenAI GPT model through LangChain.
8. The LLM generates a contextual answer.
9. The system displays the answer along with document references.

---

## RAG Pipeline

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline to answer questions from contract documents.

### 1. Document Ingestion
Users upload contract PDF files through the Streamlit interface.

### 2. Text Processing
The PDF text is extracted and split into smaller chunks to enable efficient semantic retrieval.

### 3. Embedding Generation
Each chunk is converted into vector embeddings using a sentence transformer model.

### 4. Vector Database Storage
The embeddings are stored in a **FAISS vector database**, allowing fast semantic similarity search.

### 5. Query Processing
When a user submits a question, the system converts the query into an embedding and retrieves the most relevant chunks from FAISS.

### 6. Context Augmentation
The retrieved chunks are combined with the user query and chat history to create a contextual prompt.

### 7. LLM Response Generation
The prompt and retrieved context are passed to an **OpenAI GPT model via LangChain** to generate a response.

### 8. Reference Display
The application displays the generated answer along with:

- Source document name  
- Page number used to generate the response  

This ensures **traceability and transparency** in responses.

---

## Example Use Cases

- Contract clause lookup  
- Pilot pay rate queries  
- Legal document analysis  
- Clause explanation  
- Automated contract question answering  
- Searching large collective bargaining agreements  

---

## Business / Real-World Impact

This project demonstrates how **AI-powered document intelligence systems** can help professionals quickly extract insights from large legal documents.

Organizations working with contracts often spend significant time manually searching through agreements. By combining **vector search with large language models**, this system enables users to ask questions and receive contextual answers instantly.

Potential applications include:

- Legal contract review  
- HR and labor agreement analysis  
- Compliance document search  
- Policy interpretation  
- Enterprise document intelligence systems  

---

## Disclaimer

This project is intended for **educational and research purposes only** and should not replace professional legal interpretation or legal advice.
