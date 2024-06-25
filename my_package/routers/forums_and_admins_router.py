from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter

from sqlalchemy.orm import Session

from my_package.cruds import forum_crud
from my_package.entities.e_schemas import forum_schemas
from my_package.entities.e_schemas.user_schemas import User

from my_package.auth import get_current_user
from my_package.database import get_db

forums_and_admins_router = APIRouter(
    prefix="/users", tags=["forums_and_admins"]
)
###



#forums_and_admins
@forums_and_admins_router.post("/forums_and_admins/", response_model=forum_schemas.Forum_and_adminBase)
def create_forum_and_admin(current_user: Annotated[User, Depends(get_current_user)], forum_and_admin: forum_schemas.Forum_and_adminBase, db: Session = Depends(get_db)):
    forum_crud.create_forum_and_admin(db=db, forum_and_admin=forum_and_admin)
    return 0
@forums_and_admins_router.get("/forums_and_admins/", response_model=list[forum_schemas.Forum_and_adminBase])
def read_forums_and_admins(current_user: Annotated[User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    forums = forum_crud.get_forums_and_admins(db, skip=skip, limit=limit)
    return forums
@forums_and_admins_router.get("/forum_and_admin/{forum_and_admin_id}", response_model=forum_schemas.Forum_and_admin)
def read_forum_and_admin(current_user: Annotated[User, Depends(get_current_user)], forum_and_admin_id: int, db: Session = Depends(get_db)):
    db_forum_and_admin = forum_crud.get_forum_and_admin(db, forum_and_admin_id=forum_and_admin_id)
    if db_forum_and_admin is None:
        raise HTTPException(status_code=404, detail="Forum_and_admin not found")
    return db_forum_and_admin
@forums_and_admins_router.put("/forums_and_admins/{forum_and_admin_id}", response_model=forum_schemas.Forum_and_admin)
def update_forum_and_admin(current_user: Annotated[User, Depends(get_current_user)], forum_and_admin: forum_schemas.Forum_and_adminUpdate, db: Session = Depends(get_db)):
    db_forum_and_admin = forum_crud.get_forum_and_admin(db, forum_and_admin_id=forum_and_admin.forum_and_admin_id)
    return forum_crud.update_forum_and_admin(db=db, forum_and_admin=forum_and_admin)
@forums_and_admins_router.delete("/forums_and_admins/{forum_and_admin_id}", response_model=forum_schemas.Forum_and_admin)
def delete_forum_and_admin(current_user: Annotated[User, Depends(get_current_user)], forum_and_admin_id: int, db: Session = Depends(get_db)):
    db_forum_and_admin = forum_crud.delete_forum_and_admin(db, forum_and_admin_id=forum_and_admin_id)
    return db_forum_and_admin
