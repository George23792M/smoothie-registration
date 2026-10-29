from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    DB_RETRY_ATTEMPTS: int
    DB_RETRY_MIN_WAIT: int
    DB_RETRY_MAX_WAIT: int
    DB_RETRY_MULTIPLIER: int
    
    #configuration to load from .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
settings = Settings()