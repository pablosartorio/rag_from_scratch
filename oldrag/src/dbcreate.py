import os
import hashlib
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_chroma import Chroma


# Bloque para evitar los warings por deprecated
import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)



def load_documents(docs_folder):
    """
    Dynamically loads documents from a folder, handling PDFs and text files.

    Args:
    - docs_folder (str): Path to the folder containing documents.

    Returns:
    - List of LangChain Document objects.
    """
    documents = []

    for root, _, files in os.walk(docs_folder):
        for file in files:
            file_path = os.path.join(root, file)

            # Handle PDF files
            if file.lower().endswith(".pdf"):
                print(f"Loading PDF: {file}")
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())

            # Handle text files
            elif file.lower().endswith(".txt"):
                print(f"Loading Text File: {file}")
                loader = DirectoryLoader(root, glob="*.txt")
                documents.extend(loader.load())

    return documents


def createDB(name, docs_folder):
    """
    Creates or updates a Chroma database with documents (including PDFs and text files).
    Before adding documents, it checks for duplicates to avoid loading the same content multiple times.

    Args:
    - name (str): Name of the Chroma collection (project name).
    - docs_folder (str): Folder containing the documents to process.

    Returns:
    - None
    """
    # Load documents
    print(f"Loading documents from: {docs_folder}")
    docs = load_documents(docs_folder)

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""],
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(docs)

    # Initialize embeddings
    model_kwargs = {'device': 'cpu'}
    model_name = "all-MiniLM-L6-v2"
    embeddings = SentenceTransformerEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

    # Create or update Chroma database
    db = Chroma(
        collection_name=name,
        embedding_function=embeddings,
        persist_directory=f"./{name}_chroma_db"
    )

    # Fetch existing documents to avoid duplicates
    existing = db.get()
    existing_ids = set(existing['ids']) if existing and 'ids' in existing else set()

#    # Prepare new chunks, skipping those that already exist
#    new_chunks = []
#    for chunk in chunks:
#        # Create a unique ID based on the chunk's content
#        chunk_id = hashlib.md5(chunk.page_content.encode('utf-8')).hexdigest()
#        if chunk_id not in existing_ids:
#            new_chunks.append((chunk_id, chunk))

    # Prepare new chunks, skipping those that already exist
    new_chunks = []
    for idx, chunk in enumerate(chunks):
        # Create a unique ID based on the chunk's content, file name, and chunk index
        chunk_content = chunk.page_content
        unique_str = f"{chunk_content}-{chunk.metadata.get('source', '')}-{idx}"
        chunk_id = hashlib.sha256(unique_str.encode('utf-8')).hexdigest()
        
        if chunk_id not in existing_ids:
            new_chunks.append((chunk_id, chunk))


    # Separate the IDs and chunks
    new_ids = [cid for cid, _ in new_chunks]
    new_docs = [c for _, c in new_chunks]

    # Add only new documents to the database
    if new_docs:
        db.add_documents(new_docs, ids=new_ids)
#        db.persist()
        print(f"Database '{name}' updated successfully with {len(new_docs)} new documents from {docs_folder}")
    else:
        print("No new documents to add. Database remains unchanged.")

