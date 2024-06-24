from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter

from sqlalchemy.orm import Session

from my_package import crud
from my_package.entities.e_schemas import user_schema

from my_package.auth import get_current_user
from my_package.database import get_db

user_router = APIRouter(
    prefix="/users", tags=["user"]
)

#users
@user_router.get("/{user_email}", response_model=user_schema.User)
def check_user(current_user: Annotated[user_schema.User, Depends(get_current_user)]):
    return current_user.user_id
@user_router.post("/", response_model=user_schema.User)
def create_user(current_user: Annotated[user_schema.User, Depends(get_current_user)], user: user_schema.UserCreate, db: Session = Depends(get_db) ):
    
    db_user = crud.get_user_by_email(db, user_email=user.user_email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
@user_router.get("/", response_model=list[user_schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    print("##############################")
    print(check_user())
    print("##############################")

    users = crud.get_users(db, skip=skip, limit=limit)
    return users
@user_router.get("/{user_id}", response_model=user_schema.User)
def read_user(current_user: Annotated[user_schema.User, Depends(get_current_user)], user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
@user_router.put("/{user_id}", response_model=user_schema.User)
def update_user(current_user: Annotated[user_schema.User, Depends(get_current_user)], user: user_schema.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user.user_email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.update_user(db=db, user=user)
@user_router.delete("/{user_id}", response_model=user_schema.User)
def delete_user(current_user: Annotated[user_schema.User, Depends(get_current_user)], user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    #if db_user is None:
    #    raise HTTPException(status_code=404, detail="User not found")
    return db_user
