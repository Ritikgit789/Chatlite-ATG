# model_loader.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from config import MODEL_NAME

def load_model(device: str = None):
    """
    Load tokenizer and model, possibly with quantization / device mapping.
    Returns (tokenizer, model, device_used).
    """
    # pick device
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    # Optionally use bitsandbytes quantization
    # from transformers import BitsAndBytesConfig
    # quant_config = BitsAndBytesConfig(load_in_4bit=True)
    # model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, quantization_config=quant_config, device_map="auto")

    # For simplest baseline (no quantization):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    model.to(device)

    return tokenizer, model, device

def generate_response(tokenizer, model, device, prompt: str, **gen_kwargs) -> str:
    """
    Generate continuation from prompt. Returns the newly generated text (not full prompt+text).
    """
    # Encode prompt
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=False).to(device)

    # Perform generation
    outputs = model.generate(
    **inputs,
    max_new_tokens=gen_kwargs.get("max_new_tokens", 64),
    do_sample=gen_kwargs.get("do_sample", True),
    top_k=gen_kwargs.get("top_k", 50),
    temperature=gen_kwargs.get("temperature", 0.7) if gen_kwargs.get("do_sample", True) else None,
    top_p=gen_kwargs.get("top_p", 0.9) if gen_kwargs.get("do_sample", True) else None,
    pad_token_id=tokenizer.eos_token_id,
)
    # The output includes input + generation; so we slice off the prompt part
    output_ids = outputs[0]
    # length of input:
    input_len = inputs["input_ids"].shape[1]
    new_tokens = output_ids[input_len:]
    reply = tokenizer.decode(new_tokens, skip_special_tokens=True)
    return reply



# if __name__ == "__main__":
#     from config import (
#         MAX_NEW_TOKENS,
#         TEMPERATURE,
#         TOP_P,
#         TOP_K,
#         DO_SAMPLE,
#     )

#     print("[*] Loading model...")
#     tokenizer, model, device = load_model()

#     print(f"[*] Using device: {device}")
    
#     test_prompt = """System: You are a helpful assistant.Only answer the question asked by the user. If you don't know the answer, just say that you don't know, don't try to make up an answer.

# User: What is the capital of India?
# Assistant: The capital of India is New Delhi.
# User: What is the capital of Australia?
# Assistant:The capital of Australia is Canberra.
# User: What is the capital of Canada?    
# Assistant:"""

#     print("[*] Generating response...")
#     response = generate_response(
#         tokenizer,
#         model,
#         device,
#         test_prompt,
#         max_new_tokens=MAX_NEW_TOKENS,
#         temperature=TEMPERATURE,
#         top_p=TOP_P,
#         top_k=TOP_K,
#         do_sample=DO_SAMPLE,
#     )

#     print("\n[Response]")
#     print(response)
