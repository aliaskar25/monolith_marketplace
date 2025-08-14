from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from marketplace.products.models.category_model import CategoryModel
from marketplace.products.schemas.category_dto import (
    CategoryCreateSchema,
    CategoryDTO,
    CategoryShortDTO,
    CategoryUpdateSchema,
    CategoryFiltersSchema,
)
from marketplace.products.repositories.category.abstract import CategoryRepositoryAbstract


def _to_dto(model: CategoryModel) -> CategoryDTO:
    return CategoryDTO(
        id=model.id,
        name=model.name,
        gender=model.gender,
        is_for_kids=model.is_for_kids,
        is_main_category=model.is_main_category,
        children=[CategoryShortDTO(id=child.id, name=child.name) for child in model.children],
    )


class CategoryRepository(CategoryRepositoryAbstract):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create(self, payload: CategoryCreateSchema) -> CategoryDTO:
        async with self._session_factory() as session:
            category = CategoryModel(name=payload.name)

            if payload.parents:
                parents = await session.execute(
                    select(CategoryModel).filter(CategoryModel.id.in_(payload.parents))
                )
                for parent in parents:
                    category.parents.append(parent)

            session.add(category)
            await session.flush()
            await session.commit()
            await session.refresh(category)
            return _to_dto(category)

    async def get_all(self, filters: CategoryFiltersSchema) -> List[CategoryDTO]:
        async with self._session_factory() as session:
            pass


    async def update(self, id: UUID, payload: CategoryUpdateSchema) -> Optional[CategoryDTO]:
        async with self._session_factory() as session:
            obj = await session.get(CategoryModel, id)
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
            obj = await session.get(CategoryModel, id)
            if obj is None:
                return False

            await session.delete(obj)
            await session.commit()
            return True
