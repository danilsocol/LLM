from sqlalchemy.exc import NoResultFound

from models.user import User
from typing import List, Optional

def get_all_users(session) -> List[User]:
    return session.query(User).all()

def get_users_by_organization(organization_id: int, session) -> List[User]:
    users = session.query(User).filter(User.organization_id == organization_id).all()
    return users

def get_user_by_id(id:int, session) -> Optional[User]:
    users = session.get(User, id)
    if users:
        return users
    return None

def get_user_by_email(email:str, session) -> Optional[User]:
    user = session.query(User).filter(User.email == email).first()
    if user:
        return user
    return None

def change_user_role(user_id: int, new_role: str, session) -> Optional[User]:
    user = session.get(User, user_id)
    if user:
        user.role = new_role
        session.commit()
        session.refresh(user)
        return user
    return None

def register_user(email: str, password: str, session) -> User:
    new_user = User(email = email, password = password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def login_user(email: str, password: str, session) -> Optional[User]:
    user = session.query(User).filter(User.email == email).first()
    if user and user.password == password:
        return user
    return None