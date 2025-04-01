from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from database.base import Base


class AsyncSessionManager:
    def __init__(self, database_url: str, **engine_options):
        self._engine: Optional[AsyncEngine] = None
        self._sessionmaker: Optional[async_sessionmaker] = None
        self.database_url = database_url
        self.engine_options = engine_options

    async def init(self):
        if self._engine is None or self._sessionmaker is None:
            self._engine = create_async_engine(self.database_url, **self.engine_options)
            self._sessionmaker = async_sessionmaker(
                bind=self._engine,
                expire_on_commit=False,
                autoflush=False,
            )

    async def close(self):
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._sessionmaker = None

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        if not self._sessionmaker:
            await self.init()
        if self._sessionmaker:
            async with self._sessionmaker() as session:
                try:
                    yield session
                    await session.commit()
                except Exception:
                    await session.rollback()
                    raise

    async def create_all(self):
        if self._engine:
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        if self._engine:
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            raise RuntimeError("AsyncSessionManager is not initialized")
        return self._engine
