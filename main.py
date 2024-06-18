from datetime import timedelta
from typing import Annotated

from . import schemas, auth

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user

from .database import db

app = FastAPI()

print("print")


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> auth.Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user_name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return auth.Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.user_name}]