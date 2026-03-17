import google.generativeai as genai
from app.core.config import settings
from app.services.rag_service import RAGService
from app.services import agent_tools
from typing import Dict, Any

class AgentService:
    def __init__(self, rag_service: RAGService):
        self.rag = rag_service
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        
        # Define tools accessible to the agent
        self.tools = [
            self.query_knowledge_base,
            agent_tools.get_current_time,
            agent_tools.get_rota,
            agent_tools.report_incident,
            agent_tools.get_compliance_status,
            agent_tools.calculate_training_hours
        ]
        
        self.model = genai.GenerativeModel(
            model_name="models/gemini-flash-latest", 
            tools=self.tools
        )

    def query_knowledge_base(self, query: str) -> str:
        """
        Searches the internal knowledge base for training materials (e.g. 5 levels of chunking, RAG tutorials).
        """
        import asyncio
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, self.rag.retrieve_context(query))
            return future.result()

    async def chat(self, user_message: str, history: list = None) -> str:
        """
        Starts an agentic chat session. Gemini can query RAG, fetch Rotas, or report Incidents.
        """
        chat_session = self.model.start_chat(history=history or [], enable_automatic_function_calling=True)
        response = await chat_session.send_message_async(user_message)
        return response.text
