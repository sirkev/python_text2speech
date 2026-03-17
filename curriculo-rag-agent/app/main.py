from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router as api_router

app = FastAPI(
    title="Curriculo-Agent API",
    description="A beginner-friendly Agentic RAG system for learning AI with Python.",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Curriculo-Agent API. Visit /docs for the interactive API documentation."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
