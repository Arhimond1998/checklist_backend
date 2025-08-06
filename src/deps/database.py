from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import SessionLocal

async def get_db() -> AsyncSession:  # type: ignore
    async with SessionLocal() as session:
        yield session