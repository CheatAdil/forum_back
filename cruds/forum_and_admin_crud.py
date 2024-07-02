from sqlalchemy.orm import Session

from .entities import models
from .entities.schemas import forum_and_admin_schemas

#forum and admin
def get_forum_and_admin(db: Session, forum_and_admin_id: int): #
    return db.query(models.Forum_and_admin).filter(models.Forum_and_admin.forum_and_admin_id == forum_and_admin_id).first()
def get_forums_and_admins(db: Session, skip: int = 0, limit: int = 100): #
    return db.query(models.Forum_and_admin).offset(skip).limit(limit).all()
def create_forum_and_admin(db: Session, forum_and_admin: forum_and_admin_schemas.Forum_and_adminBase): #
    db_forum_and_admin = models.Forum_and_admin(forum_id=forum_and_admin.forum_id, admin_id = forum_and_admin.admin_id)
    db.add(db_forum_and_admin)
    db.commit()
    #db.refresh(db_forum_and_admin)
    return 0
    return db_forum_and_admin
def update_forum_and_admin(db: Session, forum_and_admin: forum_and_admin_schemas.Forum_and_adminUpdate): #
    db_forum_and_admin = db.query(models.Forum_and_admin).filter(models.Forum_and_admin.forum_and_admin_id == forum_and_admin.forum_and_admin_id).first()
    db_forum_and_admin.forum_id = forum_and_admin.forum_id
    db_forum_and_admin.admin_id = forum_and_admin.admin_id
    db.commit()
    db.refresh(db_forum_and_admin)
    return db_forum_and_admin
def delete_forum_and_admin(db: Session, forum_and_admin_id: int): #
    db_forum_and_admin = db.query(models.Forum_and_admin).filter(models.Forum_and_admin.forum_and_admin_id == forum_and_admin_id).first()
    db.delete(db_forum_and_admin)
    db.commit()
    return db_forum_and_admin
