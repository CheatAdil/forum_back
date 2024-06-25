from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from my_package.cruds.user_crud import get_user_by_email
from my_package.entities import models, tokens
from my_package.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token
from my_package.database import get_db, engine

from my_package.routers.user_router import user_router
from my_package.routers.category_router import category_router
from my_package.routers.forum_router import forum_router
from my_package.routers.forums_and_admins_router import forums_and_admins_router
from my_package.routers.forum_posts_router import forum_posts_router

models.Base.metadata.create_all(bind=engine)
#yes
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login_for_access_token(
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
    return tokens.Token(access_token=access_token, token_type="bearer")

app.include_router(user_router)
app.include_router(category_router)
app.include_router(forum_router)
app.include_router(forums_and_admins_router)
app.include_router(forum_posts_router)

