from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select, func
from app.db.session import get_db
from app.db.repositories.knowledge_repo import KnowledgeRepository
from app.db.repositories.chat_repo import ChatRepository
from app.services.rag_service import RAGService
from app.services.agent_service import AgentService
from app.services.document_parser import parse_file
from app.schemas.api_models import (
    ChatRequest, ChatResponse, IngestRequest, IngestResponse,
    StatsResponse, UploadResponse, SessionResponse, MessageResponse
)
from app.models.care import Company, Branch, Employee, Client, QCIncident, IncidentStatus
from typing import List

router = APIRouter()


# --- Dependency Factories ---

def get_chat_repo(db: Session = Depends(get_db)) -> ChatRepository:
    return ChatRepository(db)

def get_agent_service(db: Session = Depends(get_db)) -> AgentService:
    repo = KnowledgeRepository(db)
    rag = RAGService(repo)
    chat_repo = ChatRepository(db)
    return AgentService(rag, chat_repo)

def get_rag_service(db: Session = Depends(get_db)) -> RAGService:
    repo = KnowledgeRepository(db)
    return RAGService(repo)


# --- Stats ---

@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """Get core metrics for the Care SaaS Dashboard."""
    try:
        companies = db.exec(select(func.count(Company.id))).one()
        branches = db.exec(select(func.count(Branch.id))).one()
        employees = db.exec(select(func.count(Employee.id))).one()
        clients = db.exec(select(func.count(Client.id))).one()
        active_incidents = db.exec(
            select(func.count(QCIncident.id))
            .where(QCIncident.status != IncidentStatus.RESOLVED)
        ).one()

        return StatsResponse(
            companies=companies,
            branches=branches,
            employees=employees,
            clients=clients,
            active_incidents=active_incidents
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Chat (with Conversation Memory) ---

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    agent: AgentService = Depends(get_agent_service)
):
    """
    Interact with the Curriculo-Agent.
    Pass a session_id to continue a previous conversation; omit it to start a new one.
    """
    try:
        response_text, session_id = await agent.chat(
            request.message,
            session_id=request.session_id,
            history=request.history
        )
        return ChatResponse(response=response_text, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Ingestion ---

@router.post("/ingest", response_model=IngestResponse)
async def ingest_content(
    request: IngestRequest,
    rag: RAGService = Depends(get_rag_service)
):
    """Ingest text content into the knowledge base."""
    try:
        chunks = await rag.ingest_text(request.text, request.source)
        return IngestResponse(
            chunks_created=chunks,
            message=f"Successfully ingested content from {request.source}."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    rag: RAGService = Depends(get_rag_service)
):
    """Upload a PDF, DOCX, or TXT file and ingest its content into the knowledge base."""
    try:
        file_bytes = await file.read()
        text, source = parse_file(file_bytes, file.content_type, file.filename)

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text content could be extracted from the file.")

        chunks = await rag.ingest_text(text, source)
        return UploadResponse(
            chunks_created=chunks,
            filename=file.filename,
            message=f"Successfully ingested {chunks} chunks from '{file.filename}'."
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Session Management ---

@router.get("/sessions", response_model=List[SessionResponse])
async def list_sessions(chat_repo: ChatRepository = Depends(get_chat_repo)):
    """List all chat sessions, most recent first."""
    sessions = chat_repo.list_sessions()
    return [SessionResponse(
        id=s.id, title=s.title, created_at=s.created_at, updated_at=s.updated_at
    ) for s in sessions]


@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
async def get_session_messages(
    session_id: str,
    chat_repo: ChatRepository = Depends(get_chat_repo)
):
    """Get all messages for a specific chat session."""
    session = chat_repo.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    messages = chat_repo.get_messages(session_id)
    return [MessageResponse(
        id=m.id, role=m.role, content=m.content, created_at=m.created_at
    ) for m in messages]


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    chat_repo: ChatRepository = Depends(get_chat_repo)
):
    """Delete a chat session and all its messages."""
    deleted = chat_repo.delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"message": f"Session {session_id} deleted."}
