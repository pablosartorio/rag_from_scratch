from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Model name
model_name = "meta-llama/Llama-3.2-3B-Instruct"

# Device setup
#device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cuda"

print("Loading the tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Set pad_token to eos_token if not defined
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("Loading the model...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
##    torch_dtype=torch.float16,
    device_map="auto"
)

# Define a prompt
prompt = "¿Cuál es la importancia histórica del aterrizaje en la luna?"
print(f"Prompt: {prompt}")

# Tokenize the input, ensuring attention_mask is set and padding works
inputs = tokenizer(prompt, return_tensors="pt", padding=True).to(device)

# Generate text with explicitly set pad_token_id
print("Generating response...")
outputs = model.generate(
    inputs.input_ids,
    attention_mask=inputs.attention_mask,  # Explicitly set the attention mask
    max_new_tokens=100,
    temperature=0.7,
    top_p=0.9,
    pad_token_id=tokenizer.pad_token_id  # Ensure pad_token_id is correctly set
)

# Decode and print the response
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"Response: {response}")

