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
from my_package.routers.token_router import token_router

models.Base.metadata.create_all(bind=engine)
#yes
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(token_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(forum_router)
app.include_router(forums_and_admins_router)
app.include_router(forum_posts_router)

