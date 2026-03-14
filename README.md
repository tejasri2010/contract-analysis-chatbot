# CBA Copilot
- Use a conda python 3.12.7 environment if you can.
- Run `pip install -r requirements.txt` to install all dependencies.
- Create a `.env` file by reffering to .env.sample file and add your OPENAI_API_KEY to it.
- Run app with `streamlit run streamlit_app.py`
- Import files into FAISS database either through upload UI or by putting files in ./files directory and running 

## Overview
Contract_chatbot_alpha is a Streamlit-based chatbot application that uses FAISS for vector-based search and retrieval. The chatbot processes user queries, retrieves relevant context from indexed documents, and provides responses with references to the source documents.

## File Descriptions

### **1. `README.md`**
- **Purpose**: Provides instructions for setting up and running the project.
- **Contents**:
  - Explains how to set up a Python environment using Conda.
  - Provides the command to install dependencies using `pip install -r requirements.txt`.
  - Describes how to run the Streamlit app using `streamlit run streamlit_app.py`.

---

### **2. `streamlit_app.py`**
- **Purpose**: The main entry point for the Streamlit-based chatbot application.
- **Key Features**:
  - Initializes the FAISS vector database using `initialize_vector_db`.
  - Allows users to upload PDF files via a sidebar and adds them to the FAISS index using `add_pdf_to_vector_db`.
  - Retrieves relevant chunks from the FAISS index for user queries using `retrieve_relevant_chunks`.
  - Displays chat history and dynamically generates responses using a language model (`ChatOpenAI`).
  - Provides references for the context used in responses, including file names and page numbers.

---

### **3. `faiss_helpers.py`**
- **Purpose**: Contains helper functions for managing the FAISS vector database.
- **Key Functions**:
  - `initialize_vector_db`: Initializes or loads an existing FAISS index and metadata store.
  - `add_pdf_to_vector_db`: Processes a PDF file, chunks its content, generates embeddings, and adds them to the FAISS index.
  - `retrieve_relevant_chunks`: Retrieves the top-k relevant chunks and their metadata based on a query string.
  - `ingest_pdfs_from_folder`: Processes all PDF files in a specified folder and adds them to the FAISS index.

---

### **4. `table_data.py`**
- **Purpose**: Provides sample table data for use in the chatbot or other parts of the application.
- **Key Functions**:
  - `get_sample_table_data`: Returns sample table data as a list of dictionaries.
  - `get_table_data_as_string`: Returns the table data as a formatted string (e.g., SQL insert statements).

---

### **5. `metadata_store.json`**
- **Purpose**: Stores metadata for the chunks added to the FAISS index.
- **Contents**:
  - Each entry includes:
    - `chunk`: The text content of the chunk.
    - `file_name`: The name of the file the chunk was extracted from.
    - `page_number`: The page number in the file where the chunk is located.
  - Enables traceability and reference for chatbot responses.

---

### **6. `requirements.txt`**
- **Purpose**: Lists the Python dependencies required for the project.
- **Contents**:
  - Includes libraries like `streamlit`, `faiss`, `sentence-transformers`, and others necessary for the chatbot and FAISS integration.

---

### **8. `.gitignore`**
- **Purpose**: Specifies intentionally untracked files to ignore in the Git repository.
- **Contents**:
  - Ignores Python cache files (`__pycache__/`, `*.py[cod]`).
  - Ignores environment files (`.env`) and directories like `files/` and `dist/`.


---

## Notes
- Ensure that the `files/` directory contains the PDF files you want to use as the knowledge base.
- The FAISS index and metadata are saved persistently, so you can continue adding documents without losing previous data.
