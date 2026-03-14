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

## Architecture Diagram

The system follows a Retrieval-Augmented Generation (RAG) architecture where uploaded contract documents are embedded into a vector database and retrieved to provide context-aware answers using a large language model.

```mermaid
flowchart LR
    A[User] --> B[Streamlit Chat Interface]
    B --> C[Upload Contract PDF]
    C --> D[Text Extraction & Chunking]
    D --> E[Embedding Generation]
    E --> F[FAISS Vector Database]

    B --> G[User Question]
    G --> H[Semantic Retrieval from FAISS]
    H --> I[Relevant Document Chunks]

    I --> J[Prompt + Context]
    J --> K[LLM (GPT Model)]
    K --> L[Generated Answer]

    L --> M[Display Answer in Chat]
    M --> N[Show Source References: Document & Page]
