# 🤖 Developer Digital Twin (RAG Agent)

A specialized conversational AI assistant built using a Retrieval-Augmented Generation (RAG) architecture. This system acts as a "digital twin," capable of answering queries based on highly specific, custom-injected context and documents.

Built with a decoupled architecture featuring a FastAPI backend for LLM orchestration and a React frontend for an interactive chat interface.

---

## 📌 Overview

This project implements an advanced LLM pipeline that connects LLaMA 3 to a local vector database. By utilizing RAG, the agent bypasses the static knowledge limitations of standard language models, retrieving relevant semantic chunks from custom data before generating accurate, context-aware responses.

---

## 🚀 Architecture & Tech Stack

* **LLM Engine:** LLaMA 3 (via Groq API for high-speed inference)
* **Orchestration:** LangChain
* **Vector Database:** ChromaDB (for semantic embedding storage and retrieval)
* **Backend Framework:** FastAPI (Python)
* **Frontend Framework:** React.js (JavaScript)
* **API Communication:** REST endpoints

---

## 🏗️ Project Creation & Structure

The repository is structured into two isolated environments for the frontend and backend:

```text
Digital-Twin/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── public/
│
└── README.md
