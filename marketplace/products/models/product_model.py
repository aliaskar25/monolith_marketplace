from uuid import uuid4, UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from marketplace.infrastructure.db_base import Base


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
