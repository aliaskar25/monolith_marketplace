from enum import Enum


class UserStatus(Enum):
    active = "active"
    disabled = "disabled"
    banned = "banned"
    pending_verification = "pending_verification"


class UserRole(Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"