from openai import OpenAI

# Set up the client with your API key
client = OpenAI(api_key="")

# Define the prompt or conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain the importance of renewable energy."}
]

# Call the API
response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # or "gpt-4"
    messages=messages,
    max_tokens=100,         # Limit the response length
    temperature=0.7,        # Controls randomness
    top_p=0.9               # Controls diversity
)

# Extract and print the response
reply = response.choices[0].message.content
print(f"ChatGPT says: {reply}")

