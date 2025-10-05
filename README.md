
# Local CLI Chatbot using Hugging Face

## 📖 Project Overview
This project is a local command-line chatbot built using a Hugging Face text generation model.  
It maintains conversational context with a sliding window memory and leverages a knowledge base for quick factual answers.  
The chatbot is modular, maintainable, and designed for easy extension.

---

# FILE STRUCTURE
```
ATG-Chatbot/
│
├── config.py           # Configuration for model parameters and memory size
├── model_loader.py     # Loads tokenizer & model; generates responses
├── chat_memory.py      # Manages conversation memory & knowledge base lookups
├── constants.py        # Knowledge base dictionary
├── interface.py        # CLI interaction loop
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
```

# 🛠 Code Structure
- config.py — Holds parameters such as model name, generation settings, and memory window size.
- model_loader.py — Loads the Hugging Face model and tokenizer, generates replies based on prompts.
- chat_memory.py — Maintains a sliding memory buffer and builds prompts for the model; integrates knowledge base checks.
- constants.py — Contains a predefined knowledge base for fast lookup.
- interface.py — The entry point for the chatbot CLI.
- requirements.txt — Lists dependencies for easy setup.
- README.md — Documentation for the project.

---

## 📌 Requirements
- Python 3.8+
- pip
- At least 4GB RAM for lightweight models; GPU recommended for faster responses
- Internet connection for downloading model weights

---

## ⚙ Installation & Setup

### Step 1 — Clone the repository
```bash
git clone https://github.com/yourusername/ATG-Chatbot.git
cd ATG-Chatbot
````

### Step 2 — Create a virtual environment (recommended)

```bash
python -m venv chatliteenv
source chatliteenv/bin/activate      # Linux / macOS
chatliteenv\Scripts\activate         # Windows
```

### Step 3 — Install requirements

```bash
pip install -r requirements.txt
```

### Step 4 — Download Hugging Face model

The model specified in `config.py` will be downloaded automatically during the first run.

---

## 🚀 How to Run

```bash
python interface.py
```

You will see:

```
🤖 Chatbot initialized! Type your message or '/exit' to quit.
```

Type your queries, for example:

```
User: What is the capital of France?
Bot: Paris.

User: What is Machine Learning?
Bot: Machine Learning is a branch of AI where systems learn from data to make predictions.

User: /exit
Exiting chatbot. Goodbye!
```

---

## 🧠 Example Interaction

```
User: What is the capital of India?
Bot: New Delhi.

User: Who are you?
Bot: I am a helpful assistant designed to answer questions and maintain conversational context.

User: What is apple?
Bot: Apple is a fruit.
```

---

## ⚠ Limitations & Known Issues

* **Model Size & Performance**: Large models like `stablelm` require significant RAM and GPU power. For lightweight models, response quality might be limited.
* **Context Limitations**: The chatbot keeps only a fixed number of recent turns (memory window). Extended context beyond that is lost.
* **Knowledge Base Coverage**: The KB is predefined and limited. Unmatched questions rely on the model’s generation, which may give incorrect answers.
* **Language Model Bias**: GPT-2 and similar models may produce biased or factually incorrect outputs.
* **Latency**: Without GPU acceleration, response generation can take several seconds for complex prompts.
* **No Persistent Memory**: Memory resets when the chatbot process is restarted.

---

## 📚 Future Improvements

* Expand the knowledge base for broader coverage
* Implement persistent memory storage
* Integrate speech-to-text and text-to-speech features
* Use a lightweight fine-tuned model for faster and more accurate responses
