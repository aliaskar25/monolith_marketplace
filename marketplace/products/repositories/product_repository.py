from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from marketplace.products.models.product_model import ProductModel
from marketplace.products.schemas.product_dto import (
    ProductDTO,
    ProductCreateSchema,
    ProductUpdateSchema,
)
from marketplace.products.repositories.abstract import ProductRepositoryAbstract


def _to_dto(model: ProductModel) -> ProductDTO:
    return ProductDTO(
        id=model.id,
        name=model.name,
    )


class ProductRepository(ProductRepositoryAbstract):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create(self, payload: ProductCreateSchema) -> ProductDTO:
        async with self._session_factory() as session:
            product = ProductModel(name=payload.name)
            session.add(product)
            await session.flush()
            await session.commit()
            await session.refresh(product)
            return _to_dto(product)

    async def get_by_id(self, id: UUID) -> Optional[ProductDTO]:
        async with self._session_factory() as session:
            obj = await session.get(ProductModel, id)
            return _to_dto(obj) if obj else None

    async def get_all(self, limit: int, offset: int) -> List[ProductDTO]:
        async with self._session_factory() as session:
            query = (
                select(ProductModel)
                .offset(offset)
                .limit(limit)
            )
            result = await session.execute(query)
            rows = result.scalars().all()
            return [_to_dto(row) for row in rows]

    async def update(self, id: UUID, payload: ProductUpdateSchema) -> Optional[ProductDTO]:
        async with self._session_factory() as session:
            obj = await session.get(ProductModel, id)
            if obj is None:
                return None
            
            update_values = payload.model_dump(exclude_unset=True)
            if "name" in update_values and update_values["name"] is not None:
                obj.name = update_values["name"]

            session.add(obj)
            await session.flush()
            await session.commit()
            await session.refresh(obj)
            return _to_dto(obj)

    async def delete(self, id: UUID) -> bool:
        async with self._session_factory() as session:
            obj = await session.get(ProductModel, id)
            if obj is None:
                return False

            await session.delete(obj)
            await session.commit()
            return True
