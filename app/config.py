from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    fb_verify_token: str
    fb_page_access_token: str
    llm_provider: str = "gemini"
    google_api_key: str
    pinecone_api_key: str
    pinecone_index_name: str = "fanpage-faqs"
    google_sheets_id: str = ""  # Default empty string allows app to load without error
    google_sheets_credentials_path: str = "credentials/service-account.json"

    class Config:
        env_file = ".env"

settings = Settings()