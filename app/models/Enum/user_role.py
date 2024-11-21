from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    ORG_ADMIN = "org_admin"
    USER = "user"
    NONE = "none"