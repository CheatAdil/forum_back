from sqlalchemy.orm import Session

from .entities import models
from .entities.schemas import category_schemas
from . import forum_crud


#category
def get_category(db: Session, category_id: int): #
    return db.query(models.Category).filter(models.Category.category_id == category_id).first()
def get_category_by_name(db: Session, category_name: str): #
    return db.query(models.Category).filter(models.Category.category_name == category_name).first()
def get_categorys(db: Session, skip: int = 0, limit: int = 100): #
    return db.query(models.Category).offset(skip).limit(limit).all()
def create_category(db: Session, category: category_schemas.CategoryCreate): #
    db_category = models.Category(category_name=category.category_name, description = category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
def update_category(db: Session, category: category_schemas.CategoryUpdate): #
    db_category = db.query(models.Category).filter(models.Category.category_id == category.category_id).first()
    db_category.category_name = category.category_name
    db_category.description = category.description
    db.commit()
    db.refresh(db_category)
    return db_category
def delete_category(db: Session, category_id: int): #
    for i in db.query(models.Forum).filter(models.Forum.forum_category == category_id).all():
        forum_crud.delete_forum(db, i.forum_id) #for cascade delete

    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    db.delete(db_category)
    db.commit()
    return db_category

