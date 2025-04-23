from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

from dotenv import load_dotenv
load_dotenv()


# Initialize ChromaDB connection
def initialize_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",                   #cómo funciona y opciones https://huggingface.co/sentence-transformers
                                         #all-mpnet-base-v2  es un modelo mas grande, reguiere GPU
        model_kwargs={"device": "cpu"}                                         #por qué cpu y no gpu?
#        model_kwargs={"device": "cuda"}                                        # usa la GPU si está disponible

    )
    db = Chroma(
        collection_name="test_collection",                                     #cambiar esto a whisper translated audio. Mejorar info extraída de whisper.
        embedding_function=embeddings,                                         #mejorar info generada a partir de audio (sentiment, ML ver)
        persist_directory="/users/psartorio/rag_from_scratch/chroma_db"        #ésta es la misma que la de los documentos, ok
    )
    return db, embeddings

# Retrieve relevant chunks
def retrieve_relevant_chunks(query, db, embeddings, k=3):
    query_embedding = embeddings.embed_query(query)
    results = db.similarity_search_by_vector(query_embedding, k=k)
    return results

# Generate augmented prompt
def generate_prompt(query, relevant_chunks):
    context = "\n".join(chunk.page_content for chunk in relevant_chunks)
#    prompt_template = (
#        "[INST] <<SYS>>\n"
#        "Usa el contexto provisto para responder la pregunta del usuario. "
#        "Si la respuesta no puede ser encontrada en el contexto, responde con \"No sé, y eso también está bien.\"\n"
#        "Context:\n"
#        "{context}\n\n"
#        "Question:\n"
#        "{query}\n"
#        "[/INST]"
#    )
    prompt_template = (
        "Usa el contexto provisto para responder la pregunta del usuario. "
        "Si la respuesta no puede ser encontrada en el contexto, responde con \"No sé, y eso también está bien.\"\n"
        "Context:\n"
        "{context}\n\n"
        "Question:\n"
        "{query}\n"
    )
    return prompt_template.format(context=context, query=query)

# Load LLaMA model
def load_model(model_name):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    return tokenizer, model, device

# Generate response from LLaMA
def generate_response(prompt, tokenizer, model, device):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True).to(device)
    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.pad_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Main query-handling function for Gradio
def question(query):
    """
    Handles a user query by interacting with the RAG pipeline.
    """
    try:
        # Initialize database and model
        db, embeddings = initialize_db()
        model_name = "meta-llama/Llama-3.2-3B-Instruct"
        tokenizer, model, device = load_model(model_name)

        # Retrieve relevant chunks
        relevant_chunks = retrieve_relevant_chunks(query, db, embeddings, k=3)

        # Generate prompt
        prompt = generate_prompt(query, relevant_chunks)

        # Generate response
        response = generate_response(prompt, tokenizer, model, device)

        return response
    except Exception as e:
        return f"Error processing query: {e}"

# Integration with Gradio
def gradio_service():
    import gradio as gr

    def process_query(user_query):
        return question(user_query)

    # Gradio Interface
    iface = gr.Interface(
        fn=process_query,
        inputs=gr.Textbox(lines=2, placeholder="Escribir la pregunta acá..."),
        outputs=gr.Textbox(label="Respuesta"),
        title="Interfaz de preguntas con RAG",
        description="Hacé una pregunta usando el sistema RAG. Las preguntas son procesadas para buscar contextos relevantes y generar una respuesta:."
    )

    iface.launch(server_name="0.0.0.0", server_port=7000)

if __name__ == "__main__":
    gradio_service()
