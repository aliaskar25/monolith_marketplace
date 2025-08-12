from fastapi import APIRouter

from marketplace.settings import settings
from marketplace.products.api.routes import router as products_router


api_router = APIRouter(prefix=settings.api_prefix)

api_router.include_router(products_router)
