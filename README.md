# 🇪🇬 Egyptian Legal Research Agent

An AI-powered legal research assistant for the **Egyptian Civil Code** that combines **Retrieval-Augmented Generation (RAG)** with **Web Search Fallback** to answer legal questions accurately.

The system first searches the local legal database. If no sufficient legal evidence is found, it automatically searches the web for additional trusted information.

---

# Features

- Egyptian Civil Law Question Answering
- Multi-Query Retrieval
- CrossEncoder Reranking
- Automatic Query Rewriting
- AI Critic Agent for Retrieval Evaluation
- Legal Report Generation
- Web Search Fallback (Tavily)
- Multi-LLM Failover (Groq → Gemini → OpenAI)
- REST API using FastAPI
- Ready for Deployment

---

# Architecture

```text
                     User Question
                           │
                           ▼
                  Orchestrator Agent
                           │
                Rewrite User Question
                           │
                           ▼
               Multi Query Generator
                           │
                           ▼
                 Local Vector Search
                     (ChromaDB)
                           │
                           ▼
                CrossEncoder Reranker
                           │
               Enough Legal Evidence?
                   │                │
                 YES               NO
                  │                 │
                  ▼                 ▼
             Critic Agent      Tavily Web Search
                  │                 │
                  └──────────┬──────┘
                             ▼
                       Writer Agent
                             │
                             ▼
                     Final Legal Answer
```

---

# Tech Stack

- Python
- FastAPI
- LangChain
- LangGraph
- ChromaDB
- HuggingFace Embeddings
- CrossEncoder Reranker
- Tavily Search API
- Groq
- Google Gemini
- OpenAI

---

# Project Structure

```text
app/
│
├── agents/
│   ├── orchestrator.py
│   ├── retriever.py
│   ├── critic.py
│   └── writer.py
│
├── llms/
│   └── provider.py
│
├── tools/
│   ├── search_documents.py
│   └── tavily_search.py
│
├── graph.py
├── main.py
├── state.py
└── questions.py

data/
├── data.pdf
└── chroma_db/

tests/
└── evaluate.py
```

---

# Workflow

### 1. User submits a legal question.

↓

### 2. Orchestrator rewrites the question into optimized legal search queries.

↓

### 3. Multi-query retrieval searches ChromaDB.

↓

### 4. CrossEncoder reranks all retrieved chunks.

↓

### 5. If enough legal evidence exists:

→ Generate the answer.

Otherwise:

↓

### 6. Search the web using Tavily.

↓

### 7. Critic Agent evaluates retrieval quality.

↓

### 8. Writer Agent generates the final legal response.

---

# Retrieval Pipeline

```
Question

↓

Query Rewriting

↓

Multi Query Retrieval

↓

Similarity Search

↓

CrossEncoder Reranking

↓

Top Legal Chunks
```

---

# LLM Routing

The project automatically switches between multiple LLM providers when one becomes unavailable or reaches its quota.

Priority:

```
Groq
   ↓
Gemini
   ↓
OpenAI
```

No code changes are required.

---

# API

### POST

```
/research
```

Request

```json
{
    "question": "ما هو عقد البيع؟"
}
```

Response

```json
{
    "original_question": "...",
    "rewritten_query": "...",
    "report": "...",
    "critique": "...",
    "queries_used": [],
    "sources": []
}
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/USERNAME/Egyptian-Legal-Research-Agent.git
```

Create environment

```bash
python -m venv research_ai
```

Activate

Windows

```bash
research_ai\Scripts\activate
```

Linux

```bash
source research_ai/bin/activate
```

Install requirements

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file

```env
TAVILY_API_KEY=
GOOGLE_API_KEY=
OPENAI_API_KEY=
GROQ_API_KEY=
```

---

# Run

```bash
uvicorn app.main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

---

# Evaluation

The project includes an automated evaluation script that runs over **100+ legal questions**.

Run

```bash
python -m app.tests.evaluate
```

Outputs

- Success Rate
- Failed Requests
- Execution Time
- Average Response Time
- JSON Results

---

# Future Improvements

- Streaming Responses
- Hybrid Retrieval (BM25 + Dense Retrieval)
- Citation Highlighting
- Legal Knowledge Graph
- Multi-document Support
- PDF Upload Interface
- Better Hallucination Detection
- Redis Caching
- Docker Support
- Railway Deployment

---


# License

This project is intended for educational and research purposes.

Legal information should not be considered professional legal advice.

---

# Author

Mohammed EL Mahdi

AI Engineer | NLP | LLM Applications | RAG Systems
