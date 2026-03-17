from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, Text
from pgvector.sqlalchemy import Vector
from datetime import datetime
from app.core.config import settings

class KnowledgeChunk(SQLModel, table=True):
    __tablename__ = "knowledge_chunks"

    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(sa_column=Column(Text, nullable=False))
    source: Optional[str] = Field(default=None)
    embedding: List[float] = Field(sa_column=Column(Vector(settings.EMBEDDING_DIMENSION)))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"<KnowledgeChunk(id={self.id}, source={self.source})>"
