from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = None

class ChatResponse(BaseModel):
    response: str

class IngestRequest(BaseModel):
    text: str
    source: str

class IngestResponse(BaseModel):
    chunks_created: int
    message: str

class StatsResponse(BaseModel):
    companies: int
    branches: int
    employees: int
    clients: int
    active_incidents: int
