<div align="center">
  
  # 🧠 SemantiCache: LLM Semantic Caching Layer
  
  ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
  ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
  ![ChromaDB](https://img.shields.io/badge/ChromaDB-13ADA0?style=for-the-badge&logo=databricks&logoColor=white)

  *An MLOps-focused infrastructure proxy that reduces LLM API costs and latency by caching semantically similar queries.*
</div>

---

## ⚡ Overview
When deploying AI/ML applications, sending repetitive or semantically identical queries to LLM APIs (like Groq, OpenAI) drains token quotas and increases response times. **SemantiCache** sits between the user and the LLM. It converts incoming prompts into vector embeddings and checks a persistent vector database (ChromaDB) for similar past queries. 

If a semantic match is found (Cache Hit), it returns the answer in milliseconds. If not (Cache Miss), it queries the LLM and saves the new response.

## ✨ Key Features
* **Semantic Matching:** Understands the *intent* of a question, not just exact keywords, using `all-MiniLM-L6-v2`.
* **Zero-Latency Responses:** Cache hits return answers in ~0.03 seconds compared to standard API waits.
* **Persistent Storage:** Utilizes **ChromaDB** to ensure memory persists across server restarts.
* **Cost Optimization:** Drastically reduces Output Tokens Per Minute (OTPM) limits on cloud LLMs.
* **Interactive UI:** Built with **Streamlit** to visually demonstrate cache hits vs. misses in real-time.
* **System Observability:** Configured with **Prometheus** metrics to track Cache Hit/Miss ratios.

---

## 📸 Project Showcase

*(Replace the links below with your actual screenshot paths after uploading them to your repo)*

### 1. The Cache Miss (Standard API Call)
> *The first time a question is asked, the system fetches the answer from the Groq API.*
<img src="link_to_your_cache_miss_screenshot.png" alt="Cache Miss" width="700"/>

### 2. The Cache Hit (Instant Response)
> *When a semantically similar question is asked, the system instantly fetches the answer from ChromaDB.*
<img src="link_to_your_cache_hit_screenshot.png" alt="Cache Hit" width="700"/>

---

## 🏗️ Architecture

1. **Frontend (Streamlit):** User interface for interacting with the AI.
2. **Backend Proxy (FastAPI):** Intercepts requests and handles the routing logic.
3. **Embedding Engine:** Translates text to vectors using HuggingFace SentenceTransformers.
4. **Vector DB (ChromaDB):** Computes cosine distance to find similarities > 75%.
5. **LLM API (Groq):** Generates responses for novel queries using `qwen/qwen3.8-27b`.

---

## 🚀 Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/yourusername/SemantiCache.git](https://github.com/yourusername/SemantiCache.git)
cd SemantiCache
