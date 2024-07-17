from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from ..cruds.user_crud import get_user_by_email
from ..entities import tokens
from ..auths.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token
from ..database import get_db

token_router = APIRouter(
    prefix="/token", tags=["token"]
)
###

@token_router.post("/")
async def login_for_access_token(response: Response, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db),
) -> tokens.Token:
    db_user = get_user_by_email(db, user_email=form_data.username)
    user = authenticate_user(db_user, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user_name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_email}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token",value=f"Bearer {access_token}", httponly=True)
    response.set_cookie(key="username",value=form_data.username, httponly=False)
    return tokens.Token(access_token=access_token, token_type="bearer")
