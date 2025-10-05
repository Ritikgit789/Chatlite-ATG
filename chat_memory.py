from collections import deque
from config import MEMORY_WINDOW
from constants import knowledge_base
import re
from fuzzywuzzy import process

def normalize_query(query: str) -> str:
    query = query.lower()
    query = re.sub(r"[^\w\s]", "", query)  # remove punctuation
    return query.strip()

class ChatMemory:
    """Maintains a sliding window of recent user–bot interactions."""

    def __init__(self, window_size: int = MEMORY_WINDOW):
        self.window_size = window_size
        self.history = deque(maxlen=window_size)

    def add_turn(self, user_text: str, bot_text: str):
        self.history.append((user_text.strip(), bot_text.strip()))

    def check_knowledge_base(self, query: str) -> str:
        normalized_query = normalize_query(query)
        best_match, score = process.extractOne(normalized_query, knowledge_base.keys())
        if score > 80:  # match threshold
            return knowledge_base[best_match]
        return None

    def build_prompt(self, current_input: str, kb_context: str = None) -> str:
        system_prompt = (
            "You are a helpful assistant that answers factual questions concisely.\n"
            "Example:\n"
            "User: What is the capital of France?\n"
            "Bot: Paris.\n"
            "User: What is the capital of India?\n"
            "Bot: New Delhi.\n"
            "User: What is Machine Learning?\n"
            "Bot: Machine Learning is a branch of AI where systems learn from data to make predictions.\n"
        )

        # Inject KB context if available
        if kb_context:
            system_prompt += f"CONTEXT: {kb_context}\n"

        history_list = list(self.history)
        # Use last 3 turns to limit prompt size
        history_text = "\n".join([f"User: {u}\nBot: {b}" for u, b in history_list[-3:]])

        return system_prompt + history_text + f"\nUser: {current_input}\nBot:"
