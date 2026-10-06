import streamlit as st
import requests
import time

# Page Setup
st.set_page_config(page_title="Semantic Cache LLM", page_icon="🧠", layout="centered")
st.title("🧠 LLM Semantic Cache Demo")
st.markdown("Ask questions and watch how the Semantic Cache saves API calls and time!")

# FastAPI Backend URL
API_URL = "http://127.0.0.1:8000/generate"

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Show Cache Hit/Miss badge if it's an assistant message
        if "source" in message:
            if message["source"] == "Cache":
                st.success(f"⚡ CACHE HIT! (Saved API Cost)")
            else:
                st.warning(f"🐌 CACHE MISS! (Used Groq API)")

# User Input
if prompt := st.chat_input("Ask something (e.g., Who is Narendra Modi?)"):
    
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # 2. Call FastAPI and show assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            start_time = time.time()
            
            try:
                # Send request to our FastAPI server
                response = requests.post(API_URL, json={"prompt": prompt})
                response_data = response.json()
                end_time = time.time()
                
                # Extract data from response
                answer = response_data.get("response", "Error generating response.")
                source = response_data.get("source", "Unknown")
                time_taken = end_time - start_time
                
                # Print the text answer
                st.markdown(answer)
                
                # Print the performance badge
                if source == "Cache":
                    st.success(f"⚡ CACHE HIT! Answered in {time_taken:.3f} seconds")
                else:
                    st.warning(f"🐌 CACHE MISS! Answered via Groq in {time_taken:.3f} seconds")
                
                # Save to history
                st.session_state.messages.append({"role": "assistant", "content": answer, "source": source})
                
            except requests.exceptions.ConnectionError:
                st.error("🚨 Connection Error: Make sure your FastAPI server is running on port 8000!")