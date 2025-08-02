from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PG_DATABASE_HOST = ''
    PG_DATABASE_PORT = ''
    PG_DATABASE_DB = ''
    PG_DATABASE_USER = ''
    PG_DATABASE_PASSWORD = ''



settings = Settings(_env_file='.env', _env_file_encoding='utf-8')