import os
import faiss
from sentence_transformers import SentenceTransformer
import json
import numpy as np

import pdfplumber
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

def chunk_text(text, chunk_size=1000, chunk_overlap=100):
    """
    Split text into chunks of approximately chunk_size characters with
    chunk_overlap characters of overlap between consecutive chunks.
    """
    chunks = []
    if len(text) <= chunk_size:
        return [text]

    start = 0
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            next_newline = text.find('\n', end - 50, end + 50)
            if next_newline != -1:
                end = next_newline
            else:
                next_period = text.find('. ', end - 50, end + 50)
                if next_period != -1:
                    end = next_period + 1
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks

def process_pdf_for_chunks(pdf_path, chunk_size=1000, chunk_overlap=100):
    """
    Process a PDF file to extract text chunks and metadata (file name and page number).
    """
    chunks_with_metadata = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                chunks = chunk_text(page_text, chunk_size, chunk_overlap)
                for chunk in chunks:
                    chunks_with_metadata.append({
                        "chunk": chunk,
                        "file_name": pdf_path,
                        "page_number": page_num + 1
                    })
    return chunks_with_metadata

def initialize_vector_db(index_path="faiss_index.bin", metadata_path="metadata_store.json", embedding_model='all-MiniLM-L6-v2'):
    """
    Initialize a FAISS vector database. If the index and metadata already exist, load them.
    Otherwise, create a new index and metadata store.
    """
    model = SentenceTransformer(embedding_model)

    # Check if the FAISS index and metadata already exist
    if os.path.exists(index_path) and os.path.exists(metadata_path):
        print("Loading existing FAISS index and metadata...")
        index = faiss.read_index(index_path)
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata_store = json.load(f)
    else:
        print("Initializing a new FAISS index and metadata store...")
        index = faiss.IndexFlatL2(model.get_sentence_embedding_dimension())
        metadata_store = []  # List to store metadata for each chunk

    return index, metadata_store, model

def add_pdf_to_vector_db(pdf_path, index, metadata_store, model, chunk_size=3000, chunk_overlap=100, metadata_path="metadata_store.json"):
    """
    Add a new PDF file to the FAISS vector database after chunking and embedding.
    """
    # Process the PDF to extract chunks and metadata
    chunks_with_metadata = process_pdf_for_chunks(pdf_path, chunk_size, chunk_overlap)
    
    # Extract chunks and metadata
    chunks = [item["chunk"] for item in chunks_with_metadata]
    metadata = [{"chunk": item["chunk"], "file_name": item["file_name"], "page_number": item["page_number"]} for item in chunks_with_metadata]
    
    # Generate embeddings for the chunks
    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype('float32')  # FAISS requires float32
    
    # Add embeddings to the FAISS index
    index.add(embeddings)
    
    # Add metadata to the metadata store
    metadata_store.extend(metadata)
    
    # Save the updated metadata to the file
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata_store, f, indent=4)
    
    print(f"Added {len(chunks)} chunks from '{pdf_path}' to the vector database.")
    return index, metadata_store

def retrieve_relevant_chunks(query, index, metadata_store, model, top_k=3):
    """
    Retrieve the top-k relevant chunks and their metadata based on a query string.
    """
    # Encode the query into an embedding
    query_embedding = model.encode([query]).astype('float32')

    # Search the FAISS index for the top-k nearest neighbors
    distances, indices = index.search(query_embedding, top_k)

    # Retrieve the corresponding chunks and metadata
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(metadata_store):  # Ensure the index is valid
            metadata = metadata_store[idx]
            results.append({
                "chunk": metadata["chunk"],
                "file_name": metadata["file_name"],
                "page_number": metadata["page_number"],
                "distance": distances[0][i]
            })

    return results

def ingest_pdfs_from_folder(folder_path, index, metadata_store, model, chunk_size=3000, chunk_overlap=100, metadata_path="metadata_store.json"):
    """
    Ingest all PDF files from a folder into the FAISS vector database.
    """
    pdf_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".pdf")]
    if not pdf_files:
        print("No PDF files found in the folder.")
        return index, metadata_store

    for pdf_file in pdf_files:
        print(f"Processing file: {pdf_file}")
        try:
            index, metadata_store = add_pdf_to_vector_db(pdf_file, index, metadata_store, model, chunk_size, chunk_overlap, metadata_path)
        except Exception as e:
            print(f"Error processing file {pdf_file}: {e}")

    print(f"Ingested {len(pdf_files)} PDF files from folder '{folder_path}'.")
    return index, metadata_store


# Example Usage
if __name__ == "__main__":
    # Initialize the vector database (load existing or create new)
    index, metadata_store, model = initialize_vector_db()

    # Ingest all PDFs from a folder
    folder_path = "./files"
    index, metadata_store = ingest_pdfs_from_folder(folder_path, index, metadata_store, model)

    # Save the FAISS index and metadata for later use
    faiss.write_index(index, "faiss_index.bin")
    with open("metadata_store.json", "w", encoding="utf-8") as f:
        json.dump(metadata_store, f, indent=4)

    # Retrieve relevant chunks for a query
    query = "What are the regulations for pilot scheduling?"
    top_k_results = retrieve_relevant_chunks(query, index, metadata_store, model, top_k=3)

    # Print the results
    print(f"Top {len(top_k_results)} results for query: '{query}'")
    for result in top_k_results:
        print(f"File: {result['file_name']}, Page: {result['page_number']}, Distance: {result['distance']:.2f}")
        print(f"Chunk: {result['chunk'][:300]}...\n")  # Print the first 300 characters of the chunk