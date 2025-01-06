from fastapi import Depends, APIRouter
from models.document import Document
from models.organization import Organization
from services.document import create_document
from services.organization import create_organization, add_user_to_organization
from services.user import register_user
from sqlmodel import Session

from database.database import get_session

from database.database import init_db

router = APIRouter()

@router.post("/test_data")
def full(session: Session = Depends(get_session)):
    init_db()

    register_user("admin@mail.ru", "12345", session)
    register_user("user@mail.ru", "12345", session)
    register_user("user1@mail.ru", "12345", session)
    register_user("user2@mail.ru", "12345", session)

    create_organization(1, Organization(name="TexnoCom"), session)

    add_user_to_organization(2, 1, session)
    add_user_to_organization(3, 1, session)
    add_user_to_organization(4, 1, session)

    document1 = Document(title="Общая документация", content="Ответы на все вопросы общей документации будет число 42",
                         organization_id=1, modified_by_id=1)
    document2 = Document(title="Докуменция по пенетрометру",
                         content="Расстояние между проколами должно быть примерно 5 га", organization_id=1,
                         modified_by_id=1)
    document3 = Document(title="Документация по архитектуре", content="Архитектура крутая вот это ваш ответ",
                         organization_id=1, modified_by_id=1)

    create_document(document1, session)
    create_document(document2, session)
    create_document(document3, session)