from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter

from sqlalchemy.orm import Session

from .cruds import forum_post_crud
from .entities.schemas import forum_post_schemas
from .entities.schemas.user_schemas import User

from .auths.get_current_user import get_current_user
from .database import get_db

forum_posts_router = APIRouter(
    prefix="/forum_posts", tags=["forum_posts"]
)
###


#forum_posts
@forum_posts_router.post("/", response_model=forum_post_schemas.Forum_postCreate)
def create_forum_post(current_user: Annotated[User, Depends(get_current_user)], forum_post: forum_post_schemas.Forum_postCreate, db: Session = Depends(get_db)):
    forum_post_crud.create_forum_post(db=db, forum_post=forum_post)
    return 0
@forum_posts_router.get("/", response_model=list[forum_post_schemas.Forum_post])
def read_forum_posts(current_user: Annotated[User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    forums = forum_post_crud.get_forum_posts(db, skip=skip, limit=limit)
    return forums
@forum_posts_router.get("/{forum_post_id}", response_model=forum_post_schemas.Forum_post)
def read_forum_post(current_user: Annotated[User, Depends(get_current_user)], forum_post_id: int, db: Session = Depends(get_db)):
    db_forum_post = forum_post_crud.get_forum_post(db, forum_post_id=forum_post_id)
    if db_forum_post is None:
        raise HTTPException(status_code=404, detail="Forum_post not found")
    return db_forum_post
@forum_posts_router.put("/{forum_post_id}", response_model=forum_post_schemas.Forum_post)
def update_forum_post(current_user: Annotated[User, Depends(get_current_user)], forum_post: forum_post_schemas.Forum_postUpdate, db: Session = Depends(get_db)):
    db_forum_post = forum_post_crud.get_forum_post(db, forum_post_id=forum_post.forum_post_id)
    return forum_post_crud.update_forum_post(db=db, forum_post=forum_post)
@forum_posts_router.delete("/{forum_post_id}", response_model=forum_post_schemas.Forum_post)
def delete_forum_post(current_user: Annotated[User, Depends(get_current_user)], forum_post_id: int, db: Session = Depends(get_db)):
    db_forum_post = forum_post_crud.delete_forum_post(db, forum_post_id=forum_post_id)
    return db_forum_post

