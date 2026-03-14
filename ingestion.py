from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader  

import os
from pinecone import Pinecone
import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv

load_dotenv()

embeddings = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

## Pinecone code:
index_name = "abr-test"

# connect to index
index = pc.Index(index_name)

# view index stats
index.describe_index_stats()

# ## Use this to upload documents as vectors
file = "./test.pdf"


loader = PyPDFLoader(file)

data = loader.load()
#print(data)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
fragments = text_splitter.split_documents(data)

print("Fragments sample:",fragments[:3])

pinecone = PineconeVectorStore.from_documents(
    fragments, embeddings, index_name=index_name
)
