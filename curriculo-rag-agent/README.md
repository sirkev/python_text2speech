# Curriculo-Agent: Beginner's Guide to Agentic RAG

Welcome to your first Agentic AI project! This project is designed to help you understand how **Retrieval Augmented Generation (RAG)** works and how to wrap it in an **Agentic Loop** using Python.

## 🚀 The Mission

Build an AI assistant that can:

1. **Read** documents (like your course materials).
2. **Remember** them by storing them in your favorite database (**Postgres**).
3. **Reason** about which information to look up to answer a user's question.

## 🛠️ The Stack

- **FastAPI**: The web framework for our API.
- **Postgres + pgvector**: Our database that can store "meaning" (vectors).
- **Google Gemini**: The brain for reasoning and creating embeddings.
- **Poetry**: Our manager for dependencies and environments.

## 📂 Layered Architecture (Controller-Service-DAO)

We are using a **Layered Architecture** to keep the code organized and scalable:

- **Controller Layer (`app/api/`)**: Handles incoming HTTP requests and responses (FastAPI Routes).
- **Service Layer (`app/services/`)**: Contains the "brain" of our app. Logic for RAG, chunking, and Agent reasoning lives here.
- **DAO Layer (`app/db/repositories/`)**: Handles all communication with Postgres.
- **Models & Schemas**: Definitions for our database tables (**Models**) and API data formats (**Schemas/DTOs**).
- **Core**: Global configuration like your Gemini API key.

## ⚙️ Setup

### 1. Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/curriculo_db
```

### 2. Install Dependencies

```bash
poetry install
```

### 3. Database Setup

Ensure you have the `pgvector` extension enabled in your Postgres database:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## 🧠 How it Works (For Beginners)

### What is RAG?

Large Language Models (LLMs) like Gemini are smart but don't know your private data. **RAG** gives them a "Reference Library" to look at before they answer.

1. **Ingest**: We break text into small chunks.
2. **Embed**: We turn those chunks into lists of numbers (vectors) that represent their meaning.
3. **Store**: We save them in Postgres.
4. **Retrieve**: When you ask a question, we find the chunks with the most similar meaning.

### What is an "Agent"?

A standard AI just answers. An **Agent** can *do things*. In this project, the agent decides *if* it needs to search the database or if it can answer from its own knowledge.

## 🛠️ Commands

- **Start the Server**: `poetry run uvicorn app.main:app --reload`
- **Run Tests**: `poetry run pytest`
