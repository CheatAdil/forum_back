from sqlalchemy.orm import Session

from .entities import models
from .entities.schemas import forum_post_schemas


def get_forum_post(db: Session, forum_post_id: int): #
    return db.query(models.Forum_post).filter(models.Forum_post.forum_post_id == forum_post_id).first()
def get_forum_posts(db: Session, skip: int = 0, limit: int = 100): #
    return db.query(models.Forum_post).offset(skip).limit(limit).all()
def create_forum_post(db: Session, forum_post: forum_post_schemas.Forum_postCreate): #
    db_forum_post = models.Forum_post(forum_id=forum_post.forum_id, user_id = forum_post.user_id, post_title = forum_post.post_title, post_content = forum_post.post_content)
    db.add(db_forum_post)
    db.commit()
    db.refresh(db_forum_post)
    return db_forum_post
def update_forum_post(db: Session, forum_post: forum_post_schemas.Forum_postUpdate): #
    db_forum_post = db.query(models.Forum_post).filter(models.Forum_post.forum_post_id == forum_post.forum_post_id).first()
    db_forum_post.post_title = forum_post.post_title
    db_forum_post.post_content = forum_post.post_content

    db.commit()
    db.refresh(db_forum_post)
    return db_forum_post
def delete_forum_post(db: Session, forum_post_id: int): #
    db_forum_post = db.query(models.Forum_post).filter(models.Forum_post.forum_post_id == forum_post_id).first()
    db.delete(db.query(models.Forum_post).filter(models.Forum_post.forum_post_id == forum_post_id).first())
    db.commit()
    return db_forum_post
