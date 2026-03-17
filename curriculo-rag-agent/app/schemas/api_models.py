from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    history: Optional[List[dict]] = None

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None

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

class UploadResponse(BaseModel):
    chunks_created: int
    filename: str
    message: str

# --- Session / Memory Schemas ---

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

class SessionResponse(BaseModel):
    id: str
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
