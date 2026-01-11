from fastapi import FastAPI
from app.models import QueryRequest, RAGResponse
from fastapi.middleware.cors import CORSMiddleware

from app.rag import ask
from app.logger import logger

app = FastAPI(title="RAG Hands on Practice with API with Logger and FastAPI, MongoDB, Supabase, External API integrated!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    logger.info("API is running.....")
    return {
        "message": "RAG Hands on With FastAPI with custom logger is running..."
    }

@app.post("/query", response_model=RAGResponse)
def query_rag(request: QueryRequest):

    logger.info(f"Received query: '{request.query}' from source: {request.source}")

    response = ask(request.query, request.source)
    logger.info(f"Response sent for query: '{request.query}'")

    return response
