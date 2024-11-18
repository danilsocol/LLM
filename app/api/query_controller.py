from typing import List

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

router = APIRouter()

@router.post("/queries/", response_model=Query)
async def create_new_query(query: Query, session: Session = Depends(get_session)):
    create_query(query, session)
    return query

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

@router.get("/organizations/{organization_id}/queries", response_model=List[Query])
async def get_organization_queries(organization_id: int, session: Session = Depends(get_session)):
    queries = get_queries_by_organization(organization_id, session)
    return queries