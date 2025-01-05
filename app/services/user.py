from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.exc import NoResultFound

from models.Enum.user_role import UserRole
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

def change_user_role(id: int, new_role: UserRole, session) -> Optional[User]:
    user = session.query(User).filter(User.id == id).first()
    if user:
        user.role = new_role
        return user
    return None

def register_user(email: str, password: str, session) -> User:
    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    new_user = User(email = email, password = hashed_password)
    print(1, email, password, new_user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def login_user(email: str, password: str, session) -> Optional[User]:
    user = session.query(User).filter(User.email == email).first()
    print(2,email,password,user)
    if user and checkpw(password.encode('utf-8'), user.password):
        return user
    return None