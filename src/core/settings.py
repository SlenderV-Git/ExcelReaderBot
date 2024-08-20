from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f'.env',
        env_file_encoding='utf-8',
    )

    BOT_TOKEN : str
    ADMIN_ID : list[int]

def get_settings() -> Settings:
    return Settings()