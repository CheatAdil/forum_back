from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
from sqlalchemy.orm import Session

from . import schemas, tokens, password_handler
from .crud import get_user_by_email
from .environment_variables import get_var

import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from .database import get_db

SECRET_KEY = get_var("SECRET_KEY")
ALGORITHM = get_var("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_var("ACCESS_TOKEN_EXPIRE_MINUTES"))
CRYPT_SCHEME = get_var("CRYPT_SCHEME")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, user_name: str, ):
    
    if get_user_by_email(db, user_email=user_name):
        user_dict = db[user_name]
        return schemas.User(**user_dict)

def authenticate_user(db_user, user_name: str, password: str):

    #print("works")
    #user = get_user(db, user_name)

    if not db_user:
        #print("not user")
        return False
    if not password_handler.verify_password(password, db_user.user_password):
        return False
    return db_user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    #print("get current user")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            print("user email is none, raising credentials_exception")
            raise credentials_exception
        token_data = tokens.TokenData(user_email=user_email)
    except jwt.exceptions.InvalidTokenError:
        print("InvalidTokenError, raising credentials_exception")
        raise credentials_exception
    user = get_user_by_email(db, user_email=token_data.user_email)
    if user is None:
        print("user is none, raising credentials_exception")
        raise credentials_exception
    yield user

async def get_current_active_user( 
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    #if current_user.disabled:
        #raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


