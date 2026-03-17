from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from app.db.session import get_db
from app.db.repositories.knowledge_repo import KnowledgeRepository
from app.services.rag_service import RAGService
from app.services.agent_service import AgentService
from app.schemas.api_models import ChatRequest, ChatResponse, IngestRequest, IngestResponse, StatsResponse
from app.models.care import Company, Branch, Employee, Client, QCIncident, IncidentStatus

router = APIRouter()

@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """
    Get core metrics for the Care SaaS Dashboard.
    """
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

def get_agent_service(db: Session = Depends(get_db)) -> AgentService:
    repo = KnowledgeRepository(db)
    rag = RAGService(repo)
    return AgentService(rag)

def get_rag_service(db: Session = Depends(get_db)) -> RAGService:
    repo = KnowledgeRepository(db)
    return RAGService(repo)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest, 
    agent: AgentService = Depends(get_agent_service)
):
    """
    Interact with the Curriculo-Agent about the ingested course materials.
    """
    try:
        response = await agent.chat(request.message, request.history)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest", response_model=IngestResponse)
async def ingest_content(
    request: IngestRequest,
    rag: RAGService = Depends(get_rag_service)
):
    """
    Ingest text content into the knowledge base.
    """
    try:
        chunks = await rag.ingest_text(request.text, request.source)
        return IngestResponse(
            chunks_created=chunks,
            message=f"Successfully ingested content from {request.source}."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
