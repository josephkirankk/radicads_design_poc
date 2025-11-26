from typing import List, Union
from pydantic import validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Radic Backend"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        elif isinstance(v, str):
            import json
            return json.loads(v)
        raise ValueError(v)

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    
    # AI - Gemini Configuration
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_NAME: str = "gemini-2.0-flash-exp"  # Working model with current API key
    GEMINI_TIMEOUT: int = 30  # Request timeout in seconds
    GEMINI_MAX_RETRIES: int = 3  # Retry attempts for transient failures

    # AI - Replicate Configuration
    REPLICATE_API_TOKEN: str = ""  # Replicate API token from replicate.com/account/api-tokens
    REPLICATE_TIMEOUT: int = 300  # Request timeout in seconds (5 minutes for long-running models)
    REPLICATE_MAX_RETRIES: int = 3  # Retry attempts for transient failures
    REPLICATE_POLL_INTERVAL: float = 0.5  # Polling interval in seconds for prediction status

    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
