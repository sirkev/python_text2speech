from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Curriculo-Agent"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/curriculo_db"
    GOOGLE_API_KEY: str = ""
    
    # Embedding configuration
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    EMBEDDING_DIMENSION: int = 3072  # Dimension for gemini-embedding-001

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
