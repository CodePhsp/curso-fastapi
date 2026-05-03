from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # SettingsConfigDict :
    # carrega as variáveis em um arquivo de configuração.

    # env_file :
    # define o caminho para arquivo de configuração
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    # Será preenchida com o valor encontrado com o mesmo nome no arquivo .env
    DATABASE_URL: str = Field(init=False)
    SECRET_KEY: str = Field(init=False)
    ALGORITHM: str = Field(init=False)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(init=False)
