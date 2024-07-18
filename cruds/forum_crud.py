from sqlalchemy.orm import Session

from ..entities import models
from ..entities.schemas import forum_schemas
from . import forum_and_admin_crud, forum_post_crud


#forum
def get_forum(db: Session, forum_id: int): #
    return db.query(models.Forum).filter(models.Forum.forum_id == forum_id).first()
def get_forum_by_name(db: Session, forum_name: str): #
    return db.query(models.Forum).filter(models.Forum.forum_name == forum_name).first()
def get_forums(db: Session, skip: int = 0, limit: int = 100): #
    return db.query(models.Forum).offset(skip).limit(limit).all()
def create_forum(db: Session, forum: forum_schemas.ForumCreate): #
    db_forum = models.Forum(forum_name=forum.forum_name, description = forum.description, forum_category = forum.forum_category)
    db.add(db_forum)
    db.commit()
    db.refresh(db_forum)
    return db_forum
def update_forum(db: Session, forum: forum_schemas.ForumUpdate): #
    db_forum = db.query(models.Forum).filter(models.Forum.forum_id == forum.forum_id).first()
    db_forum.forum_name = forum.forum_name
    db_forum.description = forum.description
    db.commit()
    db.refresh(db_forum)
    return db_forum
def delete_forum(db: Session, forum_id: int): #
    for i in db.query(models.Forum_and_admin).filter(models.Forum_and_admin.forum_id == forum_id).all():
        forum_and_admin_crud.delete_forum_and_admin(db, i.forum_and_admin_id) #for cascade delete
    
    for i in db.query(models.Forum_post).filter(models.Forum_post.forum_id == forum_id).all():
        forum_post_crud.delete_forum_post(db, i.forum_post_id) #for cascade delete
    



    db_forum = db.query(models.Forum).filter(models.Forum.forum_id == forum_id).first()
    db.delete(db_forum)
    db.commit()
    return db_forum
