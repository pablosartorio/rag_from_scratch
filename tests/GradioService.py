import gradio as gr
#from RAGService import question  # Ensure your `RAGService` has a `question` function

def query_response(query):
    try:
        # Call the RAGService's function
        return question(query)
        return print("nada")
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Define the Gradio interface
iface = gr.Interface(
    fn=query_response,
    inputs=gr.Textbox(label="Tu pregunta"),
    outputs=gr.Textbox(label="Respuesta"),
    title="Interfaz para preguntar al servicio RAG",
    description="Escribir pregunta acá para recibir una respuesta generado por IA."
)

# Launch the interface
iface.launch(server_name="0.0.0.0", server_port=7000, share=True)
