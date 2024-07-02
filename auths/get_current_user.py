from typing import Annotated
from sqlalchemy.orm import Session

from .entities import tokens
from .entities.schemas import user_schemas
from .cruds.user_crud import get_user_by_email
from .environment_variables import get_var

import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from database import get_db

SECRET_KEY = get_var("SECRET_KEY")
ALGORITHM = get_var("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    print("get current user")
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
    current_user: Annotated[user_schemas.User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


