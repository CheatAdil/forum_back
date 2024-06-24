from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, APIRouter

from sqlalchemy.orm import Session

from my_package import crud
from my_package.entities import models, schemas, tokens
from my_package.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user
from my_package.database import get_db, engine

user_router = APIRouter(
    prefix="/users", tags=["user"]
)


#users
@user_router.get("/{user_email}", response_model=schemas.User)
def check_user(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    return current_user
@user_router.post("/", response_model=schemas.User)
def create_user(current_user: Annotated[schemas.User, Depends(get_current_user)], user: schemas.UserCreate, db: Session = Depends(get_db) ):

    db_user = crud.get_user_by_email(db, user_email=user.user_email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
@user_router.get("/", response_model=list[schemas.User])
def read_users(current_user: Annotated[schemas.User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    users = crud.get_users(db, skip=skip, limit=limit)
    return users
@user_router.get("/{user_id}", response_model=schemas.User)
def read_user(current_user: Annotated[schemas.User, Depends(get_current_user)], user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
@user_router.put("/{user_id}", response_model=schemas.User)
def update_user(current_user: Annotated[schemas.User, Depends(get_current_user)], user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user.user_email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.update_user(db=db, user=user)
@user_router.delete("/{user_id}", response_model=schemas.User)
def delete_user(current_user: Annotated[schemas.User, Depends(get_current_user)], user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    #if db_user is None:
    #    raise HTTPException(status_code=404, detail="User not found")
    return db_user
