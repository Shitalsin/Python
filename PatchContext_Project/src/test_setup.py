from dotenv import load_dotenv
import os
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

# Test 1: Groq LLM
groq_client=Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_response=groq_client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Say hello in one short sentence."}]
)

print("Groq response:", chat_response.choices[0].message.content)


# Test 2: Local embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

sample_embedding=embed_model.encode("I love programming")

print("Embedding vector length:",len(sample_embedding))
print("First 5 numbers of embedding:",sample_embedding[:5])