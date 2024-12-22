import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig


class instruction:
    def __init__(self, model_id): 
        
        self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)

    def create_instruction(self, instruction, input_data=None, context=None,
                           system_prompt = "A continuación hay una instrucción que describe una tarea,    junto con una entrada que proporciona más contexto. Escriba una respuesta que complete adecuadamente la solicitud.\n\n"):
        
        sections = {"Instrucción": instruction, " Entrada": input_data, "Contexto": context,}

    
        
        prompt = system_prompt
    
        for title, content in sections.items():
            if content is not None:
                prompt += f"### {title}:\n{content}\n\n"

        prompt += "### Respuesta:\n"

        return prompt


    def generate(self, prompt, input=None, context=None,
        max_new_tokens=100,
        temperature=0.1,
        top_p=0.75,
        top_k=40,
        num_beams=2,
        **kwargs):
        """
        - Temperature: Controls randomness, higher values increase diversity.
        - Top-p (nucleus): The cumulative probability cutoff for token selection. Lower values mean sampling 
          from a smaller, more top-weighted nucleus.
        - Top-k: Sample from the k most likely next tokens at each step. Lower k focuses on higher probability tokens.

        """

        inputs = self.tokenizer(prompt, return_tensors="pt")
    
        input_ids = inputs["input_ids"].to('cuda')
    
        attention_mask = inputs["attention_mask"].to('cuda')
    
        generation_config = GenerationConfig(temperature=temperature, top_p=top_p, top_k=top_k,
        num_beams=num_beams, **kwargs,
        )
    
        with torch.no_grad():
            generation_output = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                generation_config=generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=max_new_tokens,
                early_stopping=True,
            )
        
        s = generation_output.sequences[0]
        output = self.tokenizer.decode(s)
       
        return output.split("### Respuesta:")[1].lstrip("\n")