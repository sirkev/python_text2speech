from app.db.session import engine, Base
from app.models.knowledge import KnowledgeChunk
from sqlalchemy import text

def init_db():
    with engine.connect() as conn:
        print("Checking for pgvector extension...")
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
        print("Extension verified.")

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_db()
