from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.core.config import settings

# Для SQLite используем async
engine = create_async_engine(settings.PG_DATABASE_DSN)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db() -> AsyncSession:  # type: ignore
    async with SessionLocal() as session:
        yield session
