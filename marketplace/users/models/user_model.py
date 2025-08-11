from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Index,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, validates, declarative_mixin
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.types import Enum as SQLAlchemyEnum

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from marketplace.infrastructure.db_base import Base
from marketplace.users.enums.user_enums import UserStatus, UserRole


_password_hasher = PasswordHasher()



# TODO: Move to separate file and use it in other models
@declarative_mixin
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )



class UserModel(Base, TimestampMixin):
    __tablename__ = "users"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    email: Mapped[str] = mapped_column(CITEXT, unique=True, nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    first_name: Mapped[Optional[str]] = mapped_column(String)
    last_name: Mapped[Optional[str]] = mapped_column(String)

    status: Mapped[UserStatus] = mapped_column(
        SQLAlchemyEnum(UserStatus, name="user_status"),
        server_default=UserStatus.pending_verification.value,
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(UserRole, name="user_role"),
        server_default=UserRole.user.value,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    def set_password(self, raw_password: str) -> None:
        self.hashed_password = _password_hasher.hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        try:
            _password_hasher.verify(self.hashed_password, raw_password)
        except VerifyMismatchError:
            return False

