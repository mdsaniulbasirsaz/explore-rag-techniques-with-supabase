import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from app.db import get_cursor
from app.models import RAGResponse
from app.logger import logger

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

load_dotenv()

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

llm = GeminiModel(model_name="gemini-2.5-flash")


agent = Agent(
    model=llm,
    system_prompt="You are a helpful assistant. Answer strictly based on the resume or provided context. Do not add information that is not in the context. Provide clear, concise, and professional answers about skills, experience, education, or achievements. Keep your responses focused and relevant to the query."
)

def hybrid_retrieve(query: str, source: str):
    try:
        # Encode query into embedding
        query_embedding = embedding_model.encode(query).tolist()
        query_embedding_str = str(query_embedding)  # Convert to string for SQL

        cur = get_cursor()

        cur.execute(
            """
            SELECT content, source
            FROM documents
            WHERE source = %s
            ORDER BY embedding <-> %s::vector
            LIMIT 5
            """,
            (source, query_embedding_str)
        )

        rows = cur.fetchall()
        logger.info(f"Retrieved {len(rows)} chunks for query: '{query}' from source: {source}")
        return rows

    except Exception as e:
        logger.error(f"Hybrid retrieval failed: {e}")
        return []


def ask(query: str, source: str) -> RAGResponse:
    rows = hybrid_retrieve(query, source)

    context = "\n".join([r[0] for r in rows])
    sources = list(set([r[1] for r in rows]))

    prompt = f"""
    Context:
    {context}

    Question:
    {query}
    """

    try:
        result = agent.run_sync(prompt)
        logger.info(f"Generated answer for query: '{query}'")
        return RAGResponse(answer=result.output, sources=sources)
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        return RAGResponse(answer="Error generating answer.", sources=sources)
