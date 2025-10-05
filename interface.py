# interface.py
import re
from config import MODEL_NAME, MAX_NEW_TOKENS, TEMPERATURE, TOP_P, TOP_K, DO_SAMPLE
from model_loader import load_model, generate_response
from chat_memory import ChatMemory
import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

def clean_output(text: str) -> str:
	"""Remove extra text and repetitions."""
	text = text.strip()
	text = re.split(r"\bUser:|\bBot:", text)[0]
	text = re.sub(r"(\b[A-Z][a-z]+\b.*)\1{2,}", r"\1", text)
	text = re.sub(r"[^\x00-\x7F]+", "", text)  # remove weird unicode chars
	return text.strip()
    # (No code needed here; remove $PLACEHOLDER$ and ensure correct indentation throughout the file)

print("🤖 Chatbot initialized! Type your message or '/exit' to quit.\n")


def main():
    print("Thanks for using this chatbot.")
		
tokenizer, model, device = load_model()
memory = ChatMemory()

while True:
	user_input = input("User: ").strip()
	if not user_input:
		continue
	if user_input.lower() == "/exit":
		print("Exiting chatbot. Goodbye!")
		break

	# Check KB and retrieve answer, but do NOT reply directly
	kb_answer = memory.check_knowledge_base(user_input)
	
	# NEW: Always build the prompt and generate a response from the model
	prompt = memory.build_prompt(user_input, kb_context=kb_answer) # Pass KB data as context
	
	# Generate response using the model
	bot_reply = generate_response(
		tokenizer,
		model,
		device,
		prompt,
		max_new_tokens=MAX_NEW_TOKENS,
		temperature=TEMPERATURE,
		top_p=TOP_P,
		top_k=TOP_K,
		do_sample=DO_SAMPLE,
	)
	bot_reply = clean_output(bot_reply)

	if not bot_reply and kb_answer:
		# Fallback to using the direct KB answer if the model generated nothing
		bot_reply = kb_answer 
	elif not bot_reply:
		bot_reply = "I'm sorry, I don't know the answer to that."

	print(f"Bot: {bot_reply}\n")
	memory.add_turn(user_input, bot_reply)

if __name__ == "__main__":
    main()