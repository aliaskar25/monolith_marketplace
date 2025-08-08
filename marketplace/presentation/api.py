from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from marketplace.infrastructure.db import get_session


api_router = APIRouter()


@api_router.get("/health", tags=["health"])
async def healthcheck(session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    # Быстрый пинг слоя БД через открытие сессии
    _ = session
    return {"status": "ok"}


