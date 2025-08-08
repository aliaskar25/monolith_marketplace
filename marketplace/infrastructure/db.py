from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from marketplace.settings import settings


def create_engine() -> AsyncEngine:
    return create_async_engine(settings.sqlalchemy_async_url, pool_pre_ping=True)


engine: AsyncEngine = create_engine()
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

