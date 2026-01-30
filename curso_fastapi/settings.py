from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # SettingsConfigDict :
    # carrega as variáveis em um arquivo de configuração. 

    # env_file :
    # define o caminho para arquivo de configuração
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

    # Será preenchida com o valor encontrado com o mesmo nome no arquivo .env
    DATABSE_URL: str