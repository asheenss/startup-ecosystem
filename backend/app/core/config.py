from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Startup Ecosystem API"
    app_env: str = "development"
    debug: bool = False
    database_url: str
    redis_url: str = "redis://127.0.0.1:6379/0"
    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"
    jwt_secret: str
    frontend_url: str = "http://localhost:3000"
    all_origins: list[str] = ["*"]
    upload_dir: str = "./storage/pitch-decks"
    pitch_deck_dir: str = "storage/pitch_decks"
    vector_index_path: str = "storage/pitch_vectors.index"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
