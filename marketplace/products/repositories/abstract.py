from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from marketplace.products.schemas.product_dto import (
    ProductDTO,
    ProductCreateSchema,
    ProductUpdateSchema,
)


class ProductRepositoryAbstract(ABC):
    @abstractmethod
    async def create(self, payload: ProductCreateSchema) -> ProductDTO:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[ProductDTO]:
        pass

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> List[ProductDTO]:
        pass

    @abstractmethod
    async def update(self, id: UUID, payload: ProductUpdateSchema) -> Optional[ProductDTO]:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        pass
