from transformers import AutoModelForCausalLM, AutoTokenizer
from deepspeed import init_inference

model_name = "EleutherAI/gpt-neo-2.7B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model = init_inference(model, dtype="fp16", replace_with_kernel_inject=True)

inputs = tokenizer("What is the capital of France?", return_tensors="pt").to("cuda")
outputs = model.generate(inputs.input_ids, max_new_tokens=100)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))

