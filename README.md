# 🧠 Long-Term Memory AI Assistant (RAG Implementation)

> **Hackathon Submission** | **Real-Time Memory Retention System**

## 📖 Problem Statement

Most AI models (LLMs) suffer from "Goldfish Memory"—they forget early details once the conversation exceeds their context window. Retaining information across 1,000+ turns usually requires expensive, slow context re-injection.

## 🚀 The Solution

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline that gives an AI assistant "infinite" long-term memory. It does not just "chat"; it **learns** from every interaction, stores facts in a Vector Database, and retrieves them only when relevant—ensuring low latency and high accuracy.

---

## ✨ Key Features

- **Persistent Memory:** Remembers facts (e.g., "I dislike tomatoes") across sessions and restarts.
- **Real-Time Retrieval:** Uses **ChromaDB** to fetch memories in milliseconds.
- **Contextual Awareness:** Inject relevant past details into the prompt dynamically.
- **Zero-Cost Architecture:** Built using **Groq (Llama-3)** and **HuggingFace Embeddings** (No OpenAI credits required).
- **Efficient:** Avoids token overload by retrieving only top-k relevant memories.

---

## 🛠️ Tech Stack

| Component | Technology Used        | Purpose                          |
| :-------- | :--------------------- | :------------------------------- |
| **LLM**   | **Groq (Llama-3-70b)** | High-speed inference & reasoning |

## Code Execution

- **API Key add:** [text](https://console.groq.com/keys)
- **Virtual Enviorment set up:** python -m venv venv
- **Extra Code to be run in terminal:** pip install "langchain<0.3" "langchain-community<0.3" "langchain-core<0.3" "langchain-groq<0.2" sentence-transformers chromadb
- **Execute frontend by:** python app.py
