from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Select the model name. Ensure it's a quantized or smaller version.
model_name = "meta-llama/Llama-2-7b-hf"  # Replace with the appropriate model
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load tokenizer and model
print("Loading the tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Loading the model...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # Use float16 for efficient memory usage
    device_map="auto"          # Automatically map to available devices
)

# Define the prompt
prompt = "¿Cuál es la importancia histórica del aterrizaje en la luna?"
print(f"Prompt: {prompt}")

# Tokenize the input prompt
inputs = tokenizer(prompt, return_tensors="pt").to(device)

# Generate the output
print("Generating response...")
outputs = model.generate(
    inputs.input_ids,
    max_new_tokens=100,        # Limit the length of the response
    temperature=0.7,           # Control randomness
    top_p=0.9                  # Use nucleus sampling
)

# Decode and print the response
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"Response: {response}")

