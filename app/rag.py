import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from app.db import get_cursor
from app.logger import logger
from app.models import RAGResponse

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

load_dotenv()

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

llm = GeminiModel(model_name="gemini-2.5-flash")
agent = Agent(
    model=llm,
    system_prompt="""
    You are an E-commerce assistant.
    Answer ONLY using the provided context.
    Do not guess prices, stock, or policies.
    If information is missing, say clearly: "Not available in the provided data."
    """
)

# MongoDB Setup
mongo_uri = os.getenv("MONGODB_URI")
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client.get_database("ecommerce")
products_col = mongo_db["products"]

def route_query(query: str) -> List[str]:
    q = query.lower()
    sources = []

    if any(k in q for k in ["price", "under", "cheap", "category", "product"]):
        sources.extend(["mongo", "api"])
    if any(k in q for k in ["policy", "return", "refund", "shipping", "faq", "description"]):
        sources.append("supabase")
    if not sources:
        sources.append("supabase")

    return list(set(sources))


def search_supabase(query: str, source: str = "ecommerce") -> List[str]:
    try:
        embedding = embedding_model.encode(query).tolist()
        cur = get_cursor()
        # Directly pass list if using pgvector
        cur.execute(
            """
            SELECT content
            FROM pdf1
            WHERE source = %s
            ORDER BY embedding <-> %s::vector
            LIMIT 10
            """,
            (source, embedding)
        )
        results = [r[0] for r in cur.fetchall()]
        if not results:
            logger.info(f"Supabase returned no results for query: '{query}'")
        return results
    except Exception as e:
        logger.error(f"Supabase retrieval failed: {e}")
        return []


def search_mongo(limit: int = 50) -> List[Dict]:
    try:
        results = list(
            products_col.find({}, {"_id": 0, "title": 1, "price": 1, "category": 1}).limit(limit)
        )
        return results
    except Exception as e:
        logger.error(f"MongoDB retrieval failed: {e}")
        return []

def fetch_live_products(limit: int = 50) -> List[Dict]:
    try:
        url = "https://api.escuelajs.co/api/v1/products"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        return [
            {
                "title": p.get("title"),
                "price": p.get("price"),
                "category": p.get("category", {}).get("name", "N/A")
            }
            for p in data[:limit]
        ]
    except Exception as e:
        logger.error(f"External API failed: {e}")
        return []

def build_context(docs: List[str], mongo_products: List[Dict], api_products: List[Dict]) -> str:
    context = ""

    if docs:
        context += "E-commerce Knowledge Base:\n" + "\n".join(docs)

    if mongo_products:
        context += "\n\nProduct Catalog:\n"
        for p in mongo_products:
            context += f"- {p['title']} | ${p['price']} | {p['category']}\n"

    if api_products:
        context += "\n\nLive Product Data:\n"
        for p in api_products:
            context += f"- {p['title']} | ${p['price']} | {p['category']}\n"

    return context.strip()


def ask(query: str, source: Optional[str] = None) -> RAGResponse:
    source = source or "ecommerce"
    logger.info(f"Received query: '{query}' from source: {source}")

    routes = route_query(query)

    docs, mongo_data, api_data = [], [], []

    if "supabase" in routes:
        docs = search_supabase(query, source)
    if "mongo" in routes:
        mongo_data = search_mongo(limit=50)
    if "api" in routes:
        api_data = fetch_live_products(limit=50)

    context = build_context(docs, mongo_data, api_data)

    if not context:
        logger.info(f"No relevant data found for query: '{query}'")
        return RAGResponse(answer="Not available in the provided data.", sources=routes)

    prompt = f"""
    Context:
    {context}

    User Question:
    {query}
    """

    try:
        result = agent.run_sync(prompt)
        answer = result.output or "Not available in the provided data."
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        answer = "Not available in the provided data."