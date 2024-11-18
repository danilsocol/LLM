from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.organization import Organization
    from models.query import Query

class Document(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    organization_id: int = Field(foreign_key="organization.id", index=True)
    modified_by_id: int = Field(foreign_key="user.id", index=True)

    organization: "Organization" = Relationship(back_populates="documents")
    queries: List["Query"] = Relationship(back_populates="document")