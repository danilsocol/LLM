from typing import List

from sqlmodel import Session, select
from fastapi import Depends
from fastapi import APIRouter, Depends, HTTPException
from database.database import get_session
from models.transaction import Transaction

router = APIRouter()
@router.get("/organizations/{organization_id}/transactions", response_model=List[Transaction])
def get_organization_transactions(
        organization_id: int,
        session: Session = Depends(get_session)
):
    statement = select(Transaction).where(
        Transaction.organization_id == organization_id
    ).order_by(Transaction.created_at.desc())

    transactions = session.exec(statement).all()
    return transactions