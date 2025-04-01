from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from database import database


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with database.session() as session:
        yield session
