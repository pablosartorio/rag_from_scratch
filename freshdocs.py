from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
import os
import shutil  # Para eliminar el directorio de persistencia si es necesario

def load_documents_from_folder(docs_folder):
    documents = []
    for file_name in os.listdir(docs_folder):
        file_path = os.path.join(docs_folder, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:  # Añade encoding para evitar errores
                text = f.read()
            documents.append(Document(page_content=text, metadata={"source": file_path}))
    return documents

def create_db():
    # Opcional: Eliminar el directorio de persistencia para empezar desde cero
    persist_dir = "/users/psartorio/rag_from_scratch/chroma_db"
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)  # ¡Cuidado! Esto borrará todo el contenido del directorio.

    # Cargar y dividir documentos
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    documents = load_documents_from_folder("/users/psartorio/rag_from_scratch/docs/")
    chunks = text_splitter.split_documents(documents)

    # Configurar embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    # Crear una nueva base de datos (la colección se creará desde cero)
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="test_collection",
        persist_directory=persist_dir
    )

    print("Base de datos recreada desde cero con los documentos actuales.")

create_db()
