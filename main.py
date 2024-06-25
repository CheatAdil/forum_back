from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from my_package import crud
from my_package.entities import models, schemas, tokens
from my_package.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user
from my_package.database import get_db, engine

from my_package.routers.user_router import user_router
from my_package.routers.category_router import category_router

models.Base.metadata.create_all(bind=engine)
#yes
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db),
) -> tokens.Token:
    db_user = crud.get_user_by_email(db, user_email=form_data.username)
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



#forums_and_admins
@app.post("/forums_and_admins/", response_model=schemas.Forum_and_adminBase)
def create_forum_and_admin(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_and_admin: schemas.Forum_and_adminBase, db: Session = Depends(get_db)):
    crud.create_forum_and_admin(db=db, forum_and_admin=forum_and_admin)
    return 0
@app.get("/forums_and_admins/", response_model=list[schemas.Forum_and_adminBase])
def read_forums_and_admins(current_user: Annotated[schemas.User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    forums = crud.get_forums_and_admins(db, skip=skip, limit=limit)
    return forums
@app.get("/forum_and_admin/{forum_and_admin_id}", response_model=schemas.Forum_and_admin)
def read_forum_and_admin(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_and_admin_id: int, db: Session = Depends(get_db)):
    db_forum_and_admin = crud.get_forum_and_admin(db, forum_and_admin_id=forum_and_admin_id)
    if db_forum_and_admin is None:
        raise HTTPException(status_code=404, detail="Forum_and_admin not found")
    return db_forum_and_admin
@app.put("/forums_and_admins/{forum_and_admin_id}", response_model=schemas.Forum_and_admin)
def update_forum_and_admin(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_and_admin: schemas.Forum_and_adminUpdate, db: Session = Depends(get_db)):
    db_forum_and_admin = crud.get_forum_and_admin(db, forum_and_admin_id=forum_and_admin.forum_and_admin_id)
    return crud.update_forum_and_admin(db=db, forum_and_admin=forum_and_admin)
@app.delete("/forums_and_admins/{forum_and_admin_id}", response_model=schemas.Forum_and_admin)
def delete_forum_and_admin(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_and_admin_id: int, db: Session = Depends(get_db)):
    db_forum_and_admin = crud.delete_forum_and_admin(db, forum_and_admin_id=forum_and_admin_id)
    return db_forum_and_admin

#forum_posts
@app.post("/forum_posts/", response_model=schemas.Forum_postCreate)
def create_forum_post(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_post: schemas.Forum_postCreate, db: Session = Depends(get_db)):
    crud.create_forum_post(db=db, forum_post=forum_post)
    return 0
@app.get("/forum_posts/", response_model=list[schemas.Forum_post])
def read_forum_posts(current_user: Annotated[schemas.User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    forums = crud.get_forum_posts(db, skip=skip, limit=limit)
    return forums
@app.get("/forum_post/{forum_post_id}", response_model=schemas.Forum_post)
def read_forum_post(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_post_id: int, db: Session = Depends(get_db)):
    db_forum_post = crud.get_forum_post(db, forum_post_id=forum_post_id)
    if db_forum_post is None:
        raise HTTPException(status_code=404, detail="Forum_post not found")
    return db_forum_post
@app.put("/forum_posts/{forum_post_id}", response_model=schemas.Forum_post)
def update_forum_post(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_post: schemas.Forum_postUpdate, db: Session = Depends(get_db)):
    db_forum_post = crud.get_forum_post(db, forum_post_id=forum_post.forum_post_id)
    return crud.update_forum_post(db=db, forum_post=forum_post)
@app.delete("/forum_posts/{forum_post_id}", response_model=schemas.Forum_post)
def delete_forum_post(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_post_id: int, db: Session = Depends(get_db)):
    db_forum_post = crud.delete_forum_post(db, forum_post_id=forum_post_id)
    return db_forum_post

