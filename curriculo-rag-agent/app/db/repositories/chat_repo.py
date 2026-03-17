"""
Chat Repository
Handles all database operations for ChatSession and ChatMessage.
"""

from sqlmodel import Session, select
from app.models.chat import ChatSession, ChatMessage
from typing import List, Optional
from datetime import datetime


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, title: Optional[str] = None) -> ChatSession:
        """Creates a new chat session."""
        session = ChatSession(title=title)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Gets a chat session by ID."""
        return self.db.get(ChatSession, session_id)

    def list_sessions(self, limit: int = 20) -> List[ChatSession]:
        """Lists recent chat sessions."""
        statement = select(ChatSession).order_by(ChatSession.updated_at.desc()).limit(limit)
        return self.db.exec(statement).all()

    def add_message(self, session_id: str, role: str, content: str) -> ChatMessage:
        """Adds a message to a session."""
        message = ChatMessage(session_id=session_id, role=role, content=content)
        self.db.add(message)

        # Update session timestamp
        session = self.get_session(session_id)
        if session:
            session.updated_at = datetime.utcnow()
            # Auto-title from first user message
            if session.title is None and role == "user":
                session.title = content[:80]
            self.db.add(session)

        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages(self, session_id: str, limit: int = 50) -> List[ChatMessage]:
        """Gets recent messages for a session, ordered oldest-first for conversation context."""
        statement = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        messages = self.db.exec(statement).all()
        return list(reversed(messages))  # Return in chronological order

    def delete_session(self, session_id: str) -> bool:
        """Deletes a session and all its messages."""
        session = self.get_session(session_id)
        if not session:
            return False

        # Delete messages first
        messages = self.db.exec(
            select(ChatMessage).where(ChatMessage.session_id == session_id)
        ).all()
        for msg in messages:
            self.db.delete(msg)

        self.db.delete(session)
        self.db.commit()
        return True
