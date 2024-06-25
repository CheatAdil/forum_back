from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter

from sqlalchemy.orm import Session

from my_package.cruds import forum_crud
from my_package.entities.e_schemas import forum_schemas
from my_package.entities.e_schemas.user_schemas import User

from my_package.auth import get_current_user
from my_package.database import get_db

forum_router = APIRouter(
    prefix="/users", tags=["forum"]
)
###


#forums
@forum_router.post("/forums/", response_model=forum_schemas.Forum)
def create_forum(current_user: Annotated[User, Depends(get_current_user)], forum: forum_schemas.ForumCreate, db: Session = Depends(get_db)):
    db_forum = forum_crud.get_forum_by_name(db, forum_name=forum.forum_name)
    if db_forum:
        raise HTTPException(status_code=400, detail="forum already registered")
    return forum_crud.create_forum(db=db, forum=forum)
@forum_router.get("/forums/", response_model=list[forum_schemas.Forum])
def read_forums(current_user: Annotated[User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    forums = forum_crud.get_forums(db, skip=skip, limit=limit)
    return forums
@forum_router.get("/forums/{forum_id}", response_model=forum_schemas.Forum)
def read_forum(current_user: Annotated[User, Depends(get_current_user)], forum_id: int, db: Session = Depends(get_db)):
    db_forum = forum_crud.get_forum(db, forum_id=forum_id)
    if db_forum is None:
        raise HTTPException(status_code=404, detail="Forum not found")
    return db_forum
@forum_router.put("/forums/{forum_id}", response_model=forum_schemas.Forum)
def update_forum(current_user: Annotated[User, Depends(get_current_user)], forum: forum_schemas.ForumUpdate, db: Session = Depends(get_db)):
    db_forum = forum_crud.get_forum_by_name(db, forum_name=forum.forum_name)
    #if db_forum:
        #raise HTTPException(status_code=400, detail="Email already registered")
    return forum_crud.update_forum(db=db, forum=forum)
@forum_router.delete("/forums/{forum_id}", response_model=forum_schemas.Forum)
def delete_forum(current_user: Annotated[User, Depends(get_current_user)], forum_id: int, db: Session = Depends(get_db)):
    db_forum = forum_crud.delete_forum(db, forum_id=forum_id)
    #if db_forum is None:
    #    raise HTTPException(status_code=404, detail="Forum not found")
    return db_forum
