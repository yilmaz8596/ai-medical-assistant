# 🩺 AI Medical Assistant Chatbot

An AI-powered chatbot that lets you upload medical PDF documents and ask natural-language questions about them. The assistant answers **only from the content of your documents** — it never makes up medical facts or diagnoses.

---

## Architecture

```
.
├── server/          # FastAPI backend
│   ├── main.py
│   ├── routes/
│   │   ├── upload_pdf.py    # POST /api/upload_pdf/
│   │   └── ask_question.py  # POST /api/ask/
│   ├── modules/
│   │   ├── llm.py               # Groq LLM + RAG chain (LLaMA 3.3 70B)
│   │   ├── load_vector_store.py # PDF parsing + Pinecone upsert
│   │   └── query_handlers.py    # Chain invocation
│   ├── middlewares/
│   │   └── exception_handlers.py
│   └── logger.py
└── client/          # Streamlit frontend
    ├── app.py
    ├── components/
    │   ├── chatUI.py
    │   ├── upload.py
    │   └── history_download.py
    └── utils/
        └── api.py
```

**Flow:**
1. User uploads one or more PDF files → backend chunks, embeds with Gemini (`gemini-embedding-001`), and upserts to Pinecone.
2. User asks a question → backend embeds the query, retrieves top-3 relevant chunks from Pinecone, and passes them to LLaMA 3.3 70B via Groq for a grounded answer.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| LLM | LLaMA 3.3 70B via Groq |
| Embeddings | Google Gemini (`gemini-embedding-001`) |
| Vector Store | Pinecone |
| PDF Parsing | LangChain `PyPDFLoader` |
| RAG Chain | LangChain `RetrievalQA` |

---

## Getting Started

### Prerequisites

- Python 3.10+
- [Groq API key](https://console.groq.com/)
- [Google Gemini API key](https://aistudio.google.com/app/apikey)
- [Pinecone API key](https://app.pinecone.io/) with an index of dimension `768` and metric `dotproduct`

### 1. Clone & set up the environment

```bash
git clone https://github.com/yilmaz8596/ai-medical-assistant.git
cd ai-medical-assistant
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2. Configure environment variables

Create `server/.env`:

```env
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=medical-index
PINECONE_ENV=us-east-1
```

### 3. Install dependencies & run the backend

```bash
pip install -r server/requirements.txt
uvicorn main:app --reload --app-dir server
```

API available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

### 4. Run the frontend

In a separate terminal:

```bash
pip install -r client/requirements.txt
cd client
streamlit run app.py
```

Update `client/config.py` to point to `http://127.0.0.1:8000/api` for local development.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/upload_pdf/` | Upload one or more PDF files for processing |
| `POST` | `/api/ask/` | Ask a question (form field: `question`) |

### Example: Ask a question

```bash
curl -X POST https://<your-api>/api/ask/ \
  -F "question=What are the side effects of ibuprofen?"
```

**Response:**
```json
{
  "response": "According to the documents...",
  "sources": ["uploads/doc.pdf"]
}
```

---

## Deployment

The backend is deployed on **Render** with:
- **Root Directory:** `server`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

The frontend can be deployed on **Streamlit Community Cloud** — set the main file to `client/app.py` and update `client/config.py` with your deployed backend URL.

---

## Environment Variables Reference

| Variable | Description |
|---|---|
| `GOOGLE_API_KEY` | Google Gemini API key (for embeddings) |
| `GROQ_API_KEY` | Groq API key (for LLaMA 3.3 70B) |
| `PINECONE_API_KEY` | Pinecone API key |
| `PINECONE_INDEX_NAME` | Pinecone index name (default: `medical-index`) |
| `PINECONE_ENV` | Pinecone region (default: `us-east-1`) |

---

## Disclaimer

This tool is for **informational purposes only**. It does not provide medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional.
