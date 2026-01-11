from pydantic import BaseModel
from typing import List


class QueryRequest(BaseModel):
    query: str
    source: str

class RAGResponse(BaseModel):
    answer: str
    sources: List[str]