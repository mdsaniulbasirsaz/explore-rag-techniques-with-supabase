This is a simple hands-on practice project where I explore Supabase via docker, Pydantic AI and Hybrid RAG approach. My goal is to build a lightweight pipeline that ingests PDFs, stores embeddings in Supabase (pgvector) and uses Gemini 2.5 Flash to answer queries by combining multiple retrieval sources.

## Project Structure
```
├── app/
│   ├── main.py         # FastAPI app
│   ├── db.py           # Supabase connection
│   ├── models.py       # Pydantic models
│   ├── rag.py          # Hybrid retrieval + Gemini
│   ├── ingest.py       # PDF ingestion
│   └── logger.py       # Custom logger
├── logs/               # All logs saved here
├── requirements.txt
└── .env
└── .gitignore
```

## `requirements.txt`
Open terminal and write command:
```
touch requirements.txt
```

## Setup `.env`
```
GEMINI_API_KEY=gemini-key
SUPABASE_DB_URL=postgresql://postgres:postgres@localhost:54322/postgres
LOG_LEVEL=INFO
```