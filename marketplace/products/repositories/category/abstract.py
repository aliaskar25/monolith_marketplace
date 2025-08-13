from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from marketplace.products.schemas.category_dto import (
    CategoryCreateSchema,
    CategoryDTO,
    CategoryUpdateSchema,
)


class CategoryRepositoryAbstract(ABC):
    pass