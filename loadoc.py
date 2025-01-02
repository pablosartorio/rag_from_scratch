from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
import os

# Load documents from a folder
def load_documents_from_folder(docs_folder):
    documents = []
    for file_name in os.listdir(docs_folder):
        print(file_name)
        file_path = os.path.join(docs_folder, file_name)
        print(file_path)
        if os.path.isfile(file_path):  # Ensure it's a file
            with open(file_path, "r") as f:
                text = f.read()
            documents.append(Document(page_content=text, metadata={"source": file_path}))
    return documents

# Initialize ChromaDB
def create_db():
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    documents = load_documents_from_folder("/users/psartorio/rag_from_scratch/docs/")
    chunks = text_splitter.split_documents(documents)

    # Use HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    # Initialize Chroma with persistence enabled
    db = Chroma(
        collection_name="test_collection",
        embedding_function=embeddings,
        persist_directory="/users/psartorio/rag_from_scratch/chroma_db"  # Ensure this directory exists
    )

    # Add documents to the database
    db.add_documents(chunks)

    print("Database successfully updated with persistence enabled.")

create_db()
