from typing import Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

from models.Enum.transaction_type import TransactionType

from models.organization import Organization
from models.user import User


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    organization_id: int = Field(foreign_key="organization.id")
    user_id: int = Field(foreign_key="user.id")
    type: TransactionType
    amount: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    organization: "Organization" = Relationship(back_populates="transactions")
    user: "User" = Relationship(back_populates="transactions")