from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from marketplace.products.schemas.category_dto import (
    CategoryCreateSchema,
    CategoryDTO,
    CategoryUpdateSchema,
    CategoryFiltersSchema,
)


class CategoryRepositoryAbstract(ABC):
    @abstractmethod
    async def create(self, payload: CategoryCreateSchema) -> CategoryDTO:
        pass

    @abstractmethod
    async def get_all(self, filters: CategoryFiltersSchema) -> List[CategoryDTO]:
        pass

    @abstractmethod
    async def update(self, id: UUID, payload: CategoryUpdateSchema) -> Optional[CategoryDTO]:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        pass
