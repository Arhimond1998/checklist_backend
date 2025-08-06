from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings):
    PG_DATABASE_HOST: str = ''
    PG_DATABASE_PORT: int = 5432
    PG_DATABASE_DB: str = ''
    PG_DATABASE_USER: str = ''
    PG_DATABASE_PASSWORD: str = ''
    
    @computed_field(return_type=str)
    @property
    def PG_DATABASE_DSN(self):
        return f"postgresql+asyncpg://{self.PG_DATABASE_USER}:{self.PG_DATABASE_PASSWORD}@{self.PG_DATABASE_HOST}:{self.PG_DATABASE_PORT}/{self.PG_DATABASE_DB}"
    
    SECRET_KEY: str = 'your-secret-key-in-env'
    ALGORITHM: str = 'HS256'
    



settings = Settings(_env_file='.env', _env_file_encoding='utf-8')