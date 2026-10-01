from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    LLM_API_KEY: str = "mock-key"
    LLM_BASE_URL: str = "https://gigachat.devices.sberbank.ru/api/v1"
    LLM_MODEL: str = "GigaChat"
    LLM_TIMEOUT: float = 15.0

    CACHE_TTL_SECONDS: int = 300

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()