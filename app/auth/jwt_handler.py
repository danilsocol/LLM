import os
from datetime import timedelta, datetime
from typing import Optional

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode, PyJWTError
from pydantic import BaseModel
from starlette import status

SECRET_KEY = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    id: int = None
    email: str = None

def create_access_token(email: str, id: int, expires_delta: Optional[timedelta] = None):
    data = {"email": email, "id": id}
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=algorithm)
    return encoded_jwt

def verify_access_token(token: str = Depends(oauth2_scheme)):
    print(3,token)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[algorithm])
        email: str = payload.get("email")
        id: int  = payload.get("id")
        if email is None or id is None:
            raise credentials_exception
        token_data = TokenData(id = id,email=email)
    except PyJWTError:
        raise credentials_exception
    return token_data
