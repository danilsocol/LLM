from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.database import get_session
from models.query import Query
from services.query import (
    create_query,
    get_query_by_id,
    update_query_answer,
    get_all_queries,
    get_queries_by_organization,
)

from models.organization import Organization

from models.Enum.transaction_type import TransactionType
from models.transaction import Transaction

router = APIRouter()


@router.post("/queries", response_model=Query)
async def create_query(query_data: Query, session: Session = Depends(get_session)):
    organization = session.query(Organization).filter(
        Organization.id == query_data.organization_id
    ).first()

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    if organization.coins < 20:
        raise HTTPException(
            status_code=400,
            detail="Insufficient coins. Need 20 coins to create a query."
        )

    try:
        session.begin_nested()
        query = Query(**query_data.dict())
        session.add(query)
        organization.coins -= 20
        transaction = Transaction(
            organization_id=query_data.organization_id,
            user_id=query_data.user_id,
            type=TransactionType.SPEND,
            amount=20
        )
        session.add(transaction)

        session.add(organization)
        session.commit()
        session.refresh(query)
        return query
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/queries/{query_id}", response_model=Query)
async def get_query(query_id: int, session: Session = Depends(get_session)):
    query = get_query_by_id(query_id, session)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    return query

@router.put("/queries/{query_id}/answer", response_model=Query)
async def update_query_answer_route(query_id: int, answer: str, session: Session = Depends(get_session)):
    query = update_query_answer(query_id, answer, session)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    return query

@router.get("/queries/", response_model=List[Query])
async def get_all_queries_route(session: Session = Depends(get_session)):
    queries = get_all_queries(session)
    return queries

@router.get("/queries", response_model=List[Query])
async def get_queries(
    user_id: Optional[int] = None,
    organization_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    query = session.query(Query)

    if user_id:
        query = query.filter(Query.user_id == user_id)
    if organization_id:
        query = query.filter(Query.organization_id == organization_id)

    queries = query.all()
    return queries