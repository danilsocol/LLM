from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.user import User
    from models.document import Document
    from models.organization import Organization

class Query(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    organization_id: int = Field(foreign_key="organization.id", index=True)
    document_id: Optional[int] = Field(default=None, foreign_key="document.id", index=True)

    question: str
    answer: Optional[str] = None

    user: "User" = Relationship(back_populates="queries")
    organization: "Organization" = Relationship(back_populates="queries")
    document: Optional["Document"] = Relationship(back_populates="queries")