from uuid import uuid4, UUID as PyUUID

from sqlalchemy import String, Table, Column, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.types import Enum as SQLAlchemyEnum

from marketplace.infrastructure.db_base import Base
from marketplace.products.enums.category_enums import CategoryGender


category_parents = Table(
    "category_parents",
    Base.metadata,
    Column("parent_id", PGUUID, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
    Column("child_id", PGUUID, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("parent_id", "child_id", name="uq_category_parent_child"),
)


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[PyUUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[CategoryGender] = mapped_column(
        SQLAlchemyEnum(CategoryGender, name="category_gender"),
        server_default=CategoryGender.unisex.value,
        nullable=False,
    )
    is_for_kids: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_main_category: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    parents: Mapped[list["CategoryModel"]] = relationship(
        "CategoryModel",
        secondary=category_parents,
        primaryjoin=lambda: CategoryModel.id == category_parents.c.child_id,
        secondaryjoin=lambda: CategoryModel.id == category_parents.c.parent_id,
        back_populates="children",
        lazy="selectin",
    )
    children: Mapped[list["CategoryModel"]] = relationship(
        "CategoryModel",
        secondary=category_parents,
        primaryjoin=lambda: CategoryModel.id == category_parents.c.parent_id,
        secondaryjoin=lambda: CategoryModel.id == category_parents.c.child_id,
        back_populates="parents",
        lazy="selectin",
    )
