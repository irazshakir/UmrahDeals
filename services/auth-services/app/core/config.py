from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "auth-service"
    app_port: int = 8002
    app_env: str = "development"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7



    class Config:
        env_file = ".env"

settings = Settings()
