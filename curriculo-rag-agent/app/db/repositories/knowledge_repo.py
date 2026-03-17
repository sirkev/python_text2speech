from sqlmodel import Session, select
from app.models.knowledge import KnowledgeChunk
from typing import List

class KnowledgeRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_chunks(self, chunks: List[KnowledgeChunk]):
        self.db.add_all(chunks)
        self.db.commit()

    def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[KnowledgeChunk]:
        """
        Uses pgvector's L2 distance (<->) to find the most similar chunks.
        """
        statement = select(KnowledgeChunk).order_by(
            KnowledgeChunk.embedding.l2_distance(query_embedding)
        ).limit(limit)
        return self.db.exec(statement).all()

    def delete_by_source(self, source: str):
        statement = select(KnowledgeChunk).where(KnowledgeChunk.source == source)
        results = self.db.exec(statement)
        for chunk in results:
            self.db.delete(chunk)
        self.db.commit()
