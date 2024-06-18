from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from . import schemas, auth

import jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError

from .database import db

SECRET_KEY = "803b77b07f60a79bd7fd6c163fe6b5928c85ba7fc6e7e592b2e10013f7a6be2f" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_name: Union[str, None] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, user_password):
    return pwd_context.verify(plain_password, user_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, user_name: str):
    if user_name in db:
        user_dict = db[user_name]
        return schemas.User(**user_dict)


def authenticate_user(db, user_name: str, password: str):
    user = get_user(db, user_name)
    if not user:
        return False
    if not verify_password(password, user.user_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")
        if user_name is None:
            raise credentials_exception
        token_data = auth.TokenData(user_name=user_name)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db, user_name=token_data.user_name)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user( 
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    #if current_user.disabled:
        #raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


