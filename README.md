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
```

Run
```
python app/ingest.py
```
then
```
http://localhost:54321/documents
```
![alt text](images/Supabase-Data.png)

Data Ingest Log:
![alt text](images/ingest-log.png)

# Fast API Running:
```
uvicorn app.main:app --reload
```
![alt text](images/api-running.png)
![alt text](images/api-docs.png)
![alt text](images/request-output.png)