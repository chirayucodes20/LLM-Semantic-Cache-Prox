import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Fetch and print all available models for your API key
models = client.models.list()
print("Available Models:")
for m in models.data:
    print(f"- {m.id}")