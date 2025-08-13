from typing import List, Optional
from uuid import UUID

from marketplace.products.schemas.product_dto import (
    ProductDTO,
    ProductCreateSchema,
    ProductUpdateSchema,
)
from marketplace.products.repositories.product.abstract import ProductRepositoryAbstract


class ProductService:
    def __init__(self, repository: ProductRepositoryAbstract) -> None:
        self._repository = repository

    async def create_product(self, payload: ProductCreateSchema) -> ProductDTO:
        return await self._repository.create(payload)

    async def get_product_by_id(self, id: UUID) -> Optional[ProductDTO]:
        return await self._repository.get_by_id(id)

    async def get_all_products(self, limit: int = 20, offset: int = 0) -> List[ProductDTO]:
        return await self._repository.get_all(limit, offset)

    async def update_product(self, id: UUID, payload: ProductUpdateSchema) -> Optional[ProductDTO]:
        return await self._repository.update(id, payload)

    async def delete_product(self, id: UUID) -> bool:
        return await self._repository.delete(id)
