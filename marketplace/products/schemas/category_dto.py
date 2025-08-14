from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from marketplace.products.enums.category_enums import CategoryGender


class CategoryShortDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: UUID
    name: str


class CategoryDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: UUID
    name: str
    gender: CategoryGender
    is_for_kids: bool
    is_main_category: bool
    children: list[CategoryShortDTO]


class CategoryCreateSchema(BaseModel):
    name: str
    gender: CategoryGender
    is_for_kids: bool
    is_main_category: bool
    parents: Optional[list[UUID]] = None

class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None
    gender: Optional[CategoryGender] = None
    is_for_kids: Optional[bool] = None
    is_main_category: Optional[bool] = None


class CategoryFiltersSchema(BaseModel):
    gender: Optional[CategoryGender] = None
    is_for_kids: Optional[bool] = None
