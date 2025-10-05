# config.py

# model identifier from Hugging Face hub (choose small model)
MODEL_NAME = "gpt2"  # or "distilgpt2" or any tiny model you prefer

# Generation / decoding settings
MAX_NEW_TOKENS = 50
TEMPERATURE = 0.9
TOP_P = 0.9
TOP_K = 50
DO_SAMPLE = True

# Memory / context settings
MEMORY_WINDOW = 4  # number of past *turns* (user + bot) to retain
MAX_PROMPT_TOKENS = 512  # optionally, approximate max tokens for prompt
