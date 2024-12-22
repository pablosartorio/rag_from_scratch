#!/bin/bash

# Stop the RAGService process
echo "Stopping RAGService..."
pkill -f RAGService.py
if [ $? -eq 0 ]; then
    echo "RAGService stopped successfully."
else
    echo "RAGService was not running."
fi

# Stop the GradioService process
echo "Stopping GradioService..."
pkill -f GradioService.py
if [ $? -eq 0 ]; then
    echo "GradioService stopped successfully."
else
    echo "GradioService was not running."
fi

# Stop the Chroma process
echo "Stopping Chroma service..."
pkill -f chroma
if [ $? -eq 0 ]; then
    echo "Chroma service stopped successfully."
else
    echo "Chroma service was not running."
fi

echo "All specified services have been stopped."
