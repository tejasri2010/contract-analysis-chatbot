import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import SentenceTransformerEmbeddings

from pinecone import Pinecone

from dotenv import load_dotenv

load_dotenv()
import os
import warnings
warnings.filterwarnings('ignore')

def retrieve_from_pinecone(user_query="What information do you have on Instance Sync Permissions"):
    ## Pinecone context code:
    embeddings = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')

    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

    index_name = "abr-test"

    # connect to index
    index = pc.Index(index_name)

    # view index stats
    print("Index stats:",index.describe_index_stats())

    ### Use this to retrieve from existing vector store
    pinecone = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)

    context= pinecone.similarity_search(user_query)[:10]
    return context

def retrieve_from_faiss(user_query="What information do you have on Instance Sync Permissions", 
                       index_path="faiss_index.bin", 
                       chunks_path="chunks.txt", 
                       k=10):
    """
    Retrieve relevant context from FAISS vector database
    Args:
        user_query: Input question from user
        index_path: Path to saved FAISS index
        chunks_path: Path to chunks text file
        k: Number of results to return
    Returns:
        List of relevant context chunks
    """
    try:
        # 1. Load the FAISS index
        index = faiss.read_index(index_path)
        print(f"Loaded FAISS index with {index.ntotal} vectors")

        # 2. Load the text chunks
        with open(chunks_path, "r", encoding="utf-8") as f:
            chunks_content = f.read()
        
        # Parse chunks text file
        chunks = []
        current_chunk = []
        for line in chunks_content.split('\n'):
            if line.startswith("CHUNK_"):
                if current_chunk:
                    chunks.append('\n'.join(current_chunk).strip())
                    current_chunk = []
            else:
                current_chunk.append(line)
        if current_chunk:
            chunks.append('\n'.join(current_chunk).strip())
        
        print(f"Loaded {len(chunks)} text chunks")

        # 3. Encode the query
        model = SentenceTransformer('all-MiniLM-L6-v2')
        query_embedding = model.encode([user_query])
        query_embedding = np.array(query_embedding).astype('float32')

        # 4. Search the index
        distances, indices = index.search(query_embedding, k)
        
        # 5. Get relevant contexts
        contexts = []
        for idx in indices[0]:
            if idx < len(chunks):
                contexts.append(chunks[idx])
            else:
                print(f"Warning: Index {idx} out of bounds for chunks list")
        
        return contexts[:k]

    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return []
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return []

# Example usage
if __name__ == "__main__":
    context = retrieve_from_faiss(
        user_query="What are the regulations about pilot scheduling?",
        k=5
    )
    
    print("\nTop results:")
    for i, result in enumerate(context):
        print(f"\nResult {i+1}:")
        print(result[:300] + "...")  # Show first 300 characters
