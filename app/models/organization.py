from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.user import User
    from models.document import Document
    from models.query import Query

class Organization(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    coins: int = Field(default=100)

    users: List["User"] = Relationship(back_populates="organization")
    documents: List["Document"] = Relationship(back_populates="organization")
    queries: List["Query"] = Relationship(back_populates="organization")