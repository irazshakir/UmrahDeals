# Pydantic BaseSettings for environment configs.

# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #General app settings
    app_host: str = "0.0.0.0"
    app_port: int = 8002

    #Supabase/PostgreSQL connection settings
    db_user: str
    db_password: str
    db_host: str
    db_port: int = 5432
    db_name: str = "postgres"
    service_role: str
    JWT_secret: str
    service_role: str
    jwt_secret: str

    class Config:
        env_file = ".env"
    
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

settings = Settings()
