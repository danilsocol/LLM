from typing import Optional, List

from models.query import Query


def create_query(new_query: Query, session) -> None:
    session.add(new_query)
    session.commit()
    session.refresh(new_query)

def get_query_by_id(id: int, session) -> Optional[Query]:
    query = session.get(Query, id)
    if query:
        return query
    return None

def update_query_answer(query_id: int, answer: str, session) -> Optional[Query]:
    query = session.get(Query, query_id)
    if query:
        query.answer = answer
        session.commit()
        session.refresh(query)
        return query
    return None

def get_all_queries(session) -> List[Query]:
    return session.query(Query).all()

def get_queries_by_organization(organization_id: int, session) -> List[Query]:
    return session.query(Query).filter(Query.organization_id == organization_id).all()