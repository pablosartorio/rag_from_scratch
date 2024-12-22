import gradio as gr
from RAGService import question  # Import the question function directly

# Define the response function
def response(msg, history):
    """
    Sends a user query to the RAG service and returns the response.
    """
    try:
        # Generate response using the question function
        answer = question(msg)
        return answer
    except Exception as e:
        # Return error message if RAG service fails
        return f"Error processing query: {e}"

# Create a Gradio ChatInterface
gr.ChatInterface(response).launch(server_name="0.0.0.0", server_port=7000)
