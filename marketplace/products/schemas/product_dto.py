from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: UUID
    name: str


class ProductCreateSchema(BaseModel):
    name: str


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
