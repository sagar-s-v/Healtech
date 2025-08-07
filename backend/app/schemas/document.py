from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class DocumentBase(BaseModel):
    file_name: str
    document_type: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True  # This is the correct setting

class QueryRequest(BaseModel):
    query: str
    document_id: int

class QueryResponse(BaseModel):
    answer: str
    conditions: Optional[List[str]]
    rationale: str
    retrieved_clauses: List[str]