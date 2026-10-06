from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from groq import Groq
import os
import uuid
import chromadb
from chromadb.utils import embedding_functions # NEW: Import explicitly
from dotenv import load_dotenv
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

load_dotenv()

app = FastAPI(title="LLM Semantic Cache Proxy")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Connecting to ChromaDB...")
db_client = chromadb.PersistentClient(path="./chroma_cache_db")

# NEW: Hum apna pehle se downloaded model yahan define kar rahe hain
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# NEW: ChromaDB ko force kar rahe hain yehi function use karne ke liye
collection = db_client.get_or_create_collection(
    name="semantic_cache_memory",
    embedding_function=emb_fn, 
    metadata={"hnsw:space": "cosine"} 
)
print("ChromaDB Ready!")

CACHE_HITS = Counter('llm_cache_hits_total', 'Total number of cache hits')
CACHE_MISSES = Counter('llm_cache_misses_total', 'Total number of cache misses')

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_response(request: PromptRequest):
    try:
        results = collection.query(
            query_texts=[request.prompt],
            n_results=1
        )
        
        if results['distances'] and len(results['distances'][0]) > 0:
            distance = results['distances'][0][0]
            if distance < 0.25:
                CACHE_HITS.inc()
                print(f"CACHE HIT! Distance: {distance:.2f}")
                cached_answer = results['metadatas'][0][0]["answer"]
                return {"source": "Cache", "response": cached_answer}
        
        print("CACHE MISS! Asking Groq...")
        CACHE_MISSES.inc()
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a direct, helpful assistant. Give short and precise answers."},
                {"role": "user", "content": request.prompt}
            ],
            model="qwen/qwen3.8-27b", 
            max_tokens=300,
        )
        llm_response = chat_completion.choices[0].message.content
        
        unique_id = str(uuid.uuid4())
        collection.add(
            documents=[request.prompt], 
            metadatas=[{"answer": llm_response}], 
            ids=[unique_id]
        )
        
        return {"source": "Groq LLM", "response": llm_response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)