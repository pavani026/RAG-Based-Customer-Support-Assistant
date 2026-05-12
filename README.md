# 🤖 RAG-Based Customer Support Assistant

## 📌 Project Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system that acts as an intelligent customer support assistant. Instead of relying on an LLM's memory alone, the system:

1. **Reads** a PDF knowledge base (product manuals, FAQs, policies)
2. **Stores** it as semantic embeddings in ChromaDB
3. **Retrieves** the most relevant information for each user query
4. **Generates** accurate, grounded answers using OpenAI GPT-4o-mini
5. **Escalates** to a human agent (HITL) when confidence is low

---

## 🗂️ Project Structure

```
RAG-based-customer-support-Assistant/
│
├── PDF's/
│   ├── kb.pdf                    ← Knowledge Base (what the bot reads)
│   ├── HLD_RAG_Pdf.pdf           ← High-Level Design Document
│   ├── LLD PDF.pdf               ← Low-Level Design Document
│   ├── Technical_Document.pdf    ← Full Technical Documentation
│   └── README.md                 ← PDF folder guide
│
├── db/                           ← Auto-created ChromaDB vector store
│
├── ingest.py                     ← Load PDF → Chunk → Embed → Store
├── retrieval.py                  ← Search ChromaDB for relevant chunks
├── generator.py                  ← GPT-4o-mini answer generation
├── hitl.py                       ← Human-in-the-Loop escalation
├── graph.py                      ← LangGraph 2-node workflow
├── main.py                       ← Entry point — run this!
├── requirements.txt              ← All dependencies
└── README.md                     ← This file
```

---

## ⚙️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| PDF Loader | LangChain PyPDFLoader |
| Text Splitter | RecursiveCharacterTextSplitter |
| Embedding Model | HuggingFace `all-MiniLM-L6-v2` (free, local) |
| Vector Database | ChromaDB (persisted locally) |
| LLM | OpenAI GPT-4o-mini |
| Workflow Engine | LangGraph (StateGraph) |
| HITL | Terminal-based human fallback |

---

## 🔄 System Flow

```
PDF Knowledge Base
       ↓
   ingest.py          ← Chunks + Embeds + Stores in ChromaDB (once)
       ↓
  User Question
       ↓
  LangGraph Graph
       ↓
  process_node        ← retrieval.py searches ChromaDB
       ↓
  ┌────────────────────────────┐
  │ Context found?             │
  │  YES → generate answer     │
  │  NO  → escalate = True     │
  └────────────────────────────┘
       ↓
  output_node
       ↓
  ┌────────────────────────────┐
  │ escalate == False?         │
  │  YES → print AI answer     │
  │  NO  → hitl.py (human)     │
  └────────────────────────────┘
       ↓
   Final Answer
```

---

## 🚀 Setup & Installation

### Step 1 — Clone the repository
```bash
git clone https://github.com/your-username/RAG-based-customer-support-Assistant.git
cd RAG-based-customer-support-Assistant
```

### Step 2 — Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set your OpenAI API Key

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your_openai_api_key_here
```

**Mac/Linux:**
```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

### Step 5 — Add your PDF knowledge base
```
Place your PDF file(s) inside the PDF's/ folder
Update the pdf list in main.py:
    pdfs = ["PDF's/kb.pdf"]
```

### Step 6 — Run the system
```bash
python main.py
```

---

## 💬 Sample Interaction

```
📥 Checking knowledge base...
✂️ Created 87 chunks
✅ All PDFs processed and stored successfully
🚀 System Ready!

Ask a question (or type 'exit'): What is the return policy?

💬 Final Answer:
ShopEase offers a 30-day easy return policy on most products. Items must be
unused, in original packaging, and with all tags intact.

Ask a question (or type 'exit'): How do I reset my password?

💬 Final Answer:
Click Forgot Password on the login page. Enter your registered email address.
You will receive a password reset link valid for 30 minutes.

Ask a question (or type 'exit'): What is the CEO's salary?

⚠️ Escalating to human support...
User Query: What is the CEO's salary?
👨‍💻 Enter human response: I'm sorry, that information is confidential.

💬 Final Answer:
I'm sorry, that information is confidential.
```

---

## 📐 Architecture Concepts Applied

| # | Concept | Where Applied |
|---|---------|--------------|
| 1 | What is RAG | Entire system design |
| 2 | PDF → Chunk → Embed → Store | `ingest.py` |
| 3 | Query → Retrieve → Answer | `retrieval.py` + `generator.py` |
| 4 | Graph-based workflow | `graph.py` (LangGraph) |
| 5 | 2-node flow (Input→Process→Output) | `process_node` + `output_node` |
| 6 | Conditional routing by intent | `escalate` flag in state |
| 7 | Customer Support Bot | Full system use case |
| 8 | Human-in-the-Loop (HITL) | `hitl.py` + `output_node` |

---

## 📄 Documents (PDF's/ folder)

| File | Description |
|------|-------------|
| `kb.pdf` | Knowledge base — FAQs, policies, support content the bot reads |
| `HLD_RAG_Pdf.pdf` | High-Level Design — architecture, data flow, component overview |
| `LLD PDF.pdf` | Low-Level Design — module design, data structures, routing logic |
| `Technical_Document.pdf` | Full technical documentation for engineering review |

---

## 🔑 Key Design Decisions

- **Chunk size 500, overlap 100** — balances retrieval precision and context completeness
- **Score threshold 1.5** — cosine distance cutoff; above this = irrelevant → HITL
- **all-MiniLM-L6-v2** — free local embedding model, no API cost for encoding
- **GPT-4o-mini at temperature 0.3** — factual, consistent, cost-efficient responses
- **LangGraph over simple chains** — explicit state, clean HITL routing, extensible

---

## 🛡️ Error Handling

| Scenario | Handling |
|----------|----------|
| PDF not found | try/except in ingest.py → skips file |
| No relevant chunks | retrieve_docs() returns None → HITL |
| Score too high (>1.5) | Returns None → HITL |
| LLM API failure | generate_answer() returns None → HITL |
| ChromaDB error | Returns None → HITL |

---

## 🔮 Future Enhancements

- [ ] Multi-document dynamic upload via web UI
- [ ] Async HITL via Slack/email notifications
- [ ] Conversation memory for multi-turn support
- [ ] FastAPI REST API wrapper
- [ ] Docker containerization
- [ ] Replace ChromaDB with Pinecone for production scale
- [ ] Add confidence score display to user

---

## 📋 Requirements

```
langchain
langchain-community
langchain-huggingface
langchain-chroma
langgraph
chromadb
openai
pypdf
sentence-transformers
```

---

## 👩‍💻 Author

**Pavani**  
Innomatics Research Labs — RAG Internship Project  
May 2026
