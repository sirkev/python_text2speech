import google.generativeai as genai
from app.core.config import settings
from app.db.repositories.knowledge_repo import KnowledgeRepository
from app.models.knowledge import KnowledgeChunk
from typing import List
import re

class RAGService:
    def __init__(self, repository: KnowledgeRepository):
        self.repo = repository
        genai.configure(api_key=settings.GOOGLE_API_KEY)

    async def ingest_text(self, text: str, source: str):
        """
        Ingests a large text by splitting it into semantic chunks,
        generating embeddings, and saving them to the database.
        """
        try:
            # Step 1: Simple splitting
            chunks = self._get_chunks(text)
            
            # Step 2: Generate embeddings & Create Models
            knowledge_chunks = []
            for chunk_text in chunks:
                if not chunk_text.strip():
                    continue
                    
                print(f"Generating embedding for chunk of {len(chunk_text)} chars...")
                embedding = genai.embed_content(
                    model=settings.EMBEDDING_MODEL,
                    content=chunk_text,
                    task_type="retrieval_document"
                )["embedding"]
                
                knowledge_chunks.append(
                    KnowledgeChunk(
                        content=chunk_text,
                        source=source,
                        embedding=embedding
                    )
                )
            
            # Step 3: Save to DAO
            print(f"Saving {len(knowledge_chunks)} chunks to DB...")
            self.repo.add_chunks(knowledge_chunks)
            return len(knowledge_chunks)
        except Exception as e:
            print(f"CRITICAL ERROR in ingest_text: {str(e)}")
            import traceback
            traceback.print_exc()
            raise e

    def _get_chunks(self, text: str, max_chars: int = 1000) -> List[str]:
        """
        Helper to split text into manageable chunks.
        Note: True semantic chunking would use embeddings to find breakpoints.
        This is a 'Level 2' split (recursive/sentence based) for now.
        """
        # Simple split by sentences/newlines for beginner version
        return [t.strip() for t in re.split(r'\n\n|\.\s', text) if t.strip()]

    async def retrieve_context(self, query: str, limit: int = 3) -> str:
        """
        Retrieves the most relevant chunks for a query.
        """
        query_embedding = genai.embed_content(
            model=settings.EMBEDDING_MODEL,
            content=query,
            task_type="retrieval_query"
        )["embedding"]
        
        relevant_chunks = self.repo.search_similar(query_embedding, limit=limit)
        
        context = "\n---\n".join([c.content for c in relevant_chunks])
        return context
