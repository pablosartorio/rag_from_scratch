#!/bin/bash

# Start the Chroma service
echo "Starting Chroma service..."
chroma run --path ./geco_chroma_db &
CHROMA_PID=$!
echo "Chroma service started with PID $CHROMA_PID"

# Start the RAGService
echo "Starting RAGService..."
python RAGService.py &
RAG_PID=$!
echo "RAGService started with PID $RAG_PID"

# Start the GradioService
echo "Starting GradioService..."
python GradioService.py &
GRADIO_PID=$!
echo "GradioService started with PID $GRADIO_PID"

# Trap to handle script termination
trap "echo 'Stopping services...'; kill $CHROMA_PID $RAG_PID $GRADIO_PID; exit" SIGINT SIGTERM

# Wait for all background processes
wait
