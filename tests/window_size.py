from transformers import AutoTokenizer

# Specify the model name
model_name = "meta-llama/Llama-3.2-3B-Instruct"

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Check the maximum context size
if tokenizer.model_max_length:
    print(f"The maximum token limit for the model is: {tokenizer.model_max_length} tokens.")
else:
    print("Unable to determine the maximum token limit. Check the model's documentation.")

