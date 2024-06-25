from sqlalchemy.orm import Session

from my_package.entities import models
from my_package.entities.e_schemas import user_schemas
from my_package.password_handler import get_password_hash
from . import forum_and_admin_crud


#user
def get_user(db: Session, user_id: int): #
    return db.query(models.User).filter(models.User.user_id == user_id).first()
def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.user_email == user_email).first()
def get_users(db: Session, skip: int = 0, limit: int = 100): #
    return db.query(models.User).offset(skip).limit(limit).all()
def create_user(db: Session, user: user_schemas.UserCreate): #
    db_user = models.User(user_email=user.user_email, user_password=get_password_hash(user.user_password), user_name=user.user_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def update_user(db: Session, user: user_schemas.UserUpdate): #
    db_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    db_user.user_email = user.user_email
    db_user.user_password = get_password_hash(user.user_password)
    db_user.user_name = user.user_name
    db.commit()
    db.refresh(db_user)
    return db_user
def delete_user(db: Session, user_id: int): #
    for i in db.query(models.Forum_and_admin).filter(models.Forum_and_admin.admin_id == user_id).all():
        forum_and_admin_crud.delete_forum_and_admin(db, i.forum_and_admin_id) #for cascade delete

    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()    
    db.delete(db_user)
    db.commit()
    return db_user
