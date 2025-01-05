from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from models.Enum.user_role import UserRole


if TYPE_CHECKING:
    from models.organization import Organization
    from models.query import Query
    from models.transaction import Transaction


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    role: UserRole = Field(default=UserRole.NONE)
    email: str = Field(index=True, unique=True)
    password: bytes

    organization_id: Optional[int] = Field(default=None, foreign_key="organization.id", index=True)
    organization: Optional["Organization"] = Relationship(back_populates="users")
    queries: List["Query"] = Relationship(back_populates="user")

    transactions: List["Transaction"] = Relationship(back_populates="user")