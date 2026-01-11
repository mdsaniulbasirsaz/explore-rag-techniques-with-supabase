This is a simple hands-on practice project where I explore Supabase via docker, Pydantic AI and RAG approach. My goal is to build a lightweight pipeline that ingests PDFs, stores embeddings in Supabase (pgvector) and ecommerce product list retrive via user query uses Gemini 2.5 Flash to answer queries.
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
## Architecture
![alt text](images/ecommerce-arch.png)

## Features

1. RAG system using Supabase, MongoDB, and live API data.
2. Smart query routing retrieves only the needed information.
3. FastAPI-based API with safe, context-only AI responses.
## Create python Environments
```
python3 -m venv venv
```
then
```
source venv/bin/ativate
```

## `requirements.txt`
Open terminal and write command:
```
touch requirements.txt
```
```
pip
```

## Setup `.env`
```
GEMINI_API_KEY=gemini-key
SUPABASE_DB_URL=postgresql://postgres:postgres@localhost:54322/postgres
LOG_LEVEL=INFO
MONGODB_URI
```

Run
```
python -m app.ingest
```
then
```
http://localhost:54321/documents   # Here documents is supabase table name
```

Supabas Running in Docker Container:
![alt text](images/supabase-docker.png)
![alt text](images/vector-data-pdf1.png)

![alt text](images/Supabase-Data.png)

Data Ingest Log:
![alt text](images/ingest-log.png)

# Fast API Running:
```
uvicorn app.main:app --reload
```
![alt text](images/api-running.png)
![alt text](images/api-docs.png)
and
![alt text](images/ecommer-api-docs.png)
![alt text](images/ecommer-api-endpoint.png)

Previous Practice Output:
![alt text](images/request-output.png)