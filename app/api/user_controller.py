from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.database import get_session
from models.user import User
from services.user import (
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    create_user,
    get_users_by_organization, change_user_role,
)

from app.services.user import register_user, login_user

router = APIRouter()

@router.get("/users/", response_model=List[User])
async def get_all_users_route(session: Session = Depends(get_session)):
    users = get_all_users(session)
    return users

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    user = get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/email/{email}", response_model=User)
async def get_user_by_email_route(email: str, session: Session = Depends(get_session)):
    user = get_user_by_email(email, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/organizations/{organization_id}/users", response_model=List[User])
async def get_organization_users(organization_id: int, session: Session = Depends(get_session)):
    users = get_users_by_organization(organization_id, session)
    return users

@router.put("/users/{user_id}/role", response_model=User)
async def update_user_role(user_id: int, new_role: str, session: Session = Depends(get_session)):
    updated_user = change_user_role(user_id, new_role, session)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.post("/users/register/", response_model=User)
async def register_new_user(email: str, password: str, session: Session = Depends(get_session)):
    registered_user = register_user(email,password, session)
    return registered_user

@router.post("/users/login/", response_model=User)
async def login(email: str, password: str, session: Session = Depends(get_session)):
    user = login_user(email, password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user