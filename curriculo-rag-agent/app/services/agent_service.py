import google.generativeai as genai
from app.core.config import settings
from app.services.rag_service import RAGService
from app.services import agent_tools
from app.db.repositories.chat_repo import ChatRepository
from app.core.logging import get_logger
from typing import Dict, Any, Optional, List

logger = get_logger(__name__)

class AgentService:
    def __init__(self, rag_service: RAGService, chat_repo: ChatRepository = None):
        self.rag = rag_service
        self.chat_repo = chat_repo
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        
        # Define tools accessible to the agent
        self.tools = [
            self.query_knowledge_base,
            agent_tools.get_current_time,
            agent_tools.get_rota,
            agent_tools.create_incident,
            agent_tools.get_compliance_status,
            agent_tools.calculate_training_hours,
            agent_tools.list_branches,
            agent_tools.list_branch_members,
            agent_tools.get_employee_profile,
            agent_tools.list_clients,
            agent_tools.list_incidents,
            agent_tools.generate_compliance_report,
            agent_tools.create_rota_shift
        ]
        
        self.model = genai.GenerativeModel(
            model_name="models/gemini-flash-latest", 
            tools=self.tools
        )

    def query_knowledge_base(self, query: str) -> str:
        """
        Searches the internal knowledge base for training materials (e.g. 5 levels of chunking, RAG tutorials).
        """
        logger.info("rag_query", query=query)
        import asyncio
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, self.rag.retrieve_context(query))
            return future.result()

    def _build_history_from_messages(self, messages) -> list:
        """Converts ChatMessage objects into Gemini-compatible history format."""
        history = []
        for msg in messages:
            history.append({
                "role": msg.role,
                "parts": [msg.content]
            })
        return history

    async def chat(self, user_message: str, session_id: Optional[str] = None, history: list = None) -> tuple:
        """
        Starts an agentic chat session.
        If session_id is provided and chat_repo is available, loads/saves history from DB.
        Returns (response_text, session_id).
        """
        logger.info("agent_chat_start", session_id=session_id)
        
        # If we have a session_id and a chat_repo, use server-side memory
        if session_id and self.chat_repo:
            session = self.chat_repo.get_session(session_id)
            if not session:
                logger.info("session_created", session_id=session_id)
                session = self.chat_repo.create_session()
                session_id = session.id

            messages = self.chat_repo.get_messages(session_id, limit=30)
            history = self._build_history_from_messages(messages)
            self.chat_repo.add_message(session_id, "user", user_message)

        elif not session_id and self.chat_repo:
            session = self.chat_repo.create_session()
            session_id = session.id
            logger.info("new_session_created", session_id=session_id)
            self.chat_repo.add_message(session_id, "user", user_message)
            history = []

        try:
            # Start the Gemini chat with the loaded history
            chat_session = self.model.start_chat(history=history or [], enable_automatic_function_calling=True)
            response = await chat_session.send_message_async(user_message)
            response_text = response.text
            
            logger.info("agent_response_success", session_id=session_id)
        except Exception as e:
            logger.error("agent_chat_error", session_id=session_id, error=str(e), exc_info=True)
            response_text = "I'm sorry, I encountered an error processing your request. Please try again or ask for help."

        # Save the model response
        if session_id and self.chat_repo:
            self.chat_repo.add_message(session_id, "model", response_text)

        return response_text, session_id

