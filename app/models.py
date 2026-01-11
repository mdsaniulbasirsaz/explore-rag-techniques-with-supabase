from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    query: str
    source: Optional[str] = None

class RAGResponse(BaseModel):
    answer: str
    sources: List[str]