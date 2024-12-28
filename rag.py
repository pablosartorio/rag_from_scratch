from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Initialize ChromaDB connection
def initialize_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )
    db = Chroma(
        collection_name="test_collection",
        embedding_function=embeddings,
        persist_directory="/users/psartorio/rag_from_scratch/chroma_db"
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
    prompt_template = (
        "[INST] <<SYS>>\n"
        "Usa el contexto provisto para responder la pregunta del usuario. "
        "Si la respuesta no puede ser encontrada en el contexto, responde con \"No sé, y eso también está bien.\"\n"
        "Context:\n"
        "{context}\n\n"
        "Question:\n"
        "{query}\n"
        "[/INST]"
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
        max_new_tokens=100,
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
        inputs=gr.Textbox(lines=2, placeholder="Type your question here..."),
        outputs=gr.Textbox(label="Response"),
        title="RAG Query Interface",
        description="Ask questions using the RAG system. Queries are processed to fetch relevant context and generate a response."
    )

    iface.launch(server_name="0.0.0.0", server_port=7022)

if __name__ == "__main__":
    gradio_service()
