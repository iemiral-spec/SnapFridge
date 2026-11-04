"""Uygulama ayarları (ortam değişkenlerinden okunur). Sahibi: Ahmet İlker (konfigürasyon)."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Yerelde hızlı başlamak için SQLite; Render'da PostgreSQL adresi verilir.
    database_url: str = "sqlite:///./snapfridge.db"
    jwt_secret: str = "dev-only-secret-change-me"
    jwt_expire_minutes: int = 60 * 24
    vision_provider: str = "mock"
    vision_api_key: str = ""
    cors_origins: str = "http://localhost:5173"
    max_upload_bytes: int = 10 * 1024 * 1024  # 10 MB (plan: NFR Security)


settings = Settings()
