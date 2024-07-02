from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter

from sqlalchemy.orm import Session

from .cruds import category_crud
from .entities.schemas import category_schemas
from .entities.schemas.user_schemas import User

from .auths.get_current_user import get_current_user
from .database import get_db

category_router = APIRouter(
    prefix="/categories", tags=["category"]
)
###




#categories
@category_router.post("/", response_model=category_schemas.Category)
def create_category(current_user: Annotated[User, Depends(get_current_user)], category: category_schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = category_crud.get_category_by_name(db, category_name=category.category_name)
    if db_category:
        raise HTTPException(status_code=400, detail="category already registered")
    return category_crud.create_category(db=db, category=category)
@category_router.get("/", response_model=list[category_schemas.Category])
def read_categorys(current_user: Annotated[User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = category_crud.get_categorys(db, skip=skip, limit=limit)
    return categories
@category_router.get("/{category_id}", response_model=category_schemas.Category)
def read_category(current_user: Annotated[User, Depends(get_current_user)], category_id: int, db: Session = Depends(get_db)):
    db_category = category_crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category
@category_router.put("/{category_id}", response_model=category_schemas.Category)
def update_category(current_user: Annotated[User, Depends(get_current_user)], category: category_schemas.CategoryUpdate, db: Session = Depends(get_db)):
    db_category = category_crud.get_category_by_name(db, category_name=category.category_name)
    #if db_category:
        #raise HTTPException(status_code=400, detail="Email already registered")
    return category_crud.update_category(db=db, category=category)
@category_router.delete("/{category_id}", response_model=category_schemas.Category)
def delete_category(current_user: Annotated[User, Depends(get_current_user)], category_id: int, db: Session = Depends(get_db)):
    db_category = category_crud.delete_category(db, category_id=category_id)
    #if db_category is None:
    #    raise HTTPException(status_code=404, detail="Category not found")
    return db_category
