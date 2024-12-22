from fastapi import FastAPI, Response
from langchain_community.embeddings import SentenceTransformerEmbeddings
#from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from text_generation import Client
import chromadb
import requests
import json
from chromadb.config import Settings

from templates import llama3_prompt_template

# Opción para manejar proxy
import os

# Unset proxy environment variables
os.environ.pop("ALL_PROXY", None)
os.environ.pop("all_proxy", None)


# Configuración de servicios
chroma_host='localhost'

chroma_port=8000

#rest_host='0.0.0.0'
#rest_port=8001

llm_server_host = "http://127.0.0.1:11434"

app = FastAPI()

# Cliente LLM
client = Client(llm_server_host, timeout=90)

def create_retriever():
    """
    Crea un retriever RAG
    """
    model_kwargs = {'device': 'cpu'}

    model_name="all-MiniLM-L6-v2"

    embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs
    )

#    chroma_client = chromadb.HttpClient(
#            host=chroma_host,
#            port=chroma_port
#    )

    # Use persistent client with explicit directory
    chroma_client = chromadb.PersistentClient(
        path="./geco_chroma_db",  # Specify your collection's directory
        settings=Settings(
            anonymized_telemetry=False,  # Optional: disable telemetry
            allow_reset=True  # Allows resetting the database if needed
        )
    )

    db = Chroma(
        client=chroma_client,
        collection_name='geco',
        embedding_function=embeddings,
    )

    return db.as_retriever(search_kwargs={"k": 6})


retriever=create_retriever()

def context_gen(doc):
    """
    Esta función sirve para generar la el contexto que se envia al
    modelo de lenguaje utilizando los chunks
    """
    contexto=''

    for _, chunk in enumerate(doc):
        contexto+=(f'{chunk.page_content} ')

    return contexto

def generate_prompt(msg, context):
    """
    La siguiente función genera el prompt a enviar al LLM.
    El template depende del modelo LLM utilizado.
    """
    return llama3_prompt_template.replace("#prompt#", msg).replace("#context#", context)

def question(query):
    """
    Generate a response for a query.
    """
    query = query.lower()
    docs = retriever.get_relevant_documents(query)
    context = context_gen(docs[:3])
    prompt = generate_prompt(msg=query, context=context)
    print(prompt)

    # Prepare the payload
    payload = {
        "model": "llama3.2",  # Specify the model name
        "prompt": prompt,
        "max_new_tokens": 1000,
        "temperature": 0
    }

    try:
        # Send the request to Ollama
        response = requests.post(f"{llm_server_host}/api/generate", json=payload, stream=True)

        # Handle streaming response
        answer = ""
        for chunk in response.iter_lines():
            if chunk:
                data = json.loads(chunk)
                answer += data.get("response", "")

    except Exception as e:
        print(f"Error during LLM generation: {e}")
        answer = "Lo siento, hubo un error al procesar tu consulta."

    print(answer)
    return answer



#@app.get("/")
#def return_answer(msg: str):
#    answer=question(msg)
#    return Response(answer, media_type="text/plain")
#
#
#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host=rest_host, port=rest_port)
