import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    model: str = os.getenv("LLM_MODEL", "claude-sonnet-5-5")
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "2500"))
    cors_origins: list[str] = [
        o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if o.strip()
    ]
    max_image_mb: int = int(os.getenv("MAX_IMAGE_MB", "5"))


settings = Settings()
