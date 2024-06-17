from sqlalchemy.orm import Session

from . import models, schemas
from .hash import get_password_hash

def get_user(db: Session, user_id: int): #
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.user_email == user_email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100): #
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate): #
    db_user = models.User(user_email=user.user_email, user_password=get_password_hash(user.user_password), user_name=user.user_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schemas.UserUpdate): #
    db_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    db_user.user_email = user.user_email
    db_user.user_password = get_password_hash(user.user_password)
    db_user.user_name = user.user_name
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int): #
    for i in db.query(models.Forum_and_admin).filter(models.Forum_and_admin.admin_id == user_id).all():
        delete_forum_and_admin(db, i.forum_and_admin_id) #for cascade delete

    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()    
    db.delete(db_user)
    db.commit()
    return db_user



def get_category(db: Session, category_id: int): #
    return db.query(models.Category).filter(models.Category.category_id == category_id).first()

def get_category_by_name(db: Session, category_name: str): #
    return db.query(models.Category).filter(models.Category.category_name == category_name).first()

def get_categorys(db: Session, skip: int = 0, limit: int = 100): #
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate): #
    db_category = models.Category(category_name=category.category_name, description = category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category: schemas.CategoryUpdate): #
    db_category = db.query(models.Category).filter(models.Category.category_id == category.category_id).first()
    db_category.category_name = category.category_name
    db_category.description = category.description
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int): #
    for i in db.query(models.Forum).filter(models.Forum.forum_category == category_id).all():
        delete_forum(db, i.forum_id) #for cascade delete

    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    db.delete(db_category)
    db.commit()
    return db_category



def get_forum(db: Session, forum_id: int): #
    return db.query(models.Forum).filter(models.Forum.forum_id == forum_id).first()

def get_forum_by_name(db: Session, forum_name: str): #
    return db.query(models.Forum).filter(models.Forum.forum_name == forum_name).first()

def get_forums(db: Session, skip: int = 0, limit: int = 100): #
    return db.query(models.Forum).offset(skip).limit(limit).all()

def create_forum(db: Session, forum: schemas.ForumCreate): #
    db_forum = models.Forum(forum_name=forum.forum_name, description = forum.description, forum_category = forum.forum_category)
    db.add(db_forum)
    db.commit()
    db.refresh(db_forum)
    return db_forum

def update_forum(db: Session, forum: schemas.ForumUpdate): #
    db_forum = db.query(models.Forum).filter(models.Forum.forum_id == forum.forum_id).first()
    db_forum.forum_name = forum.forum_name
    db_forum.description = forum.description
    db.commit()
    db.refresh(db_forum)
    return db_forum

def delete_forum(db: Session, forum_id: int): #
    for i in db.query(models.Forum_and_admin).filter(models.Forum_and_admin.forum_id == forum_id).all():
        delete_forum_and_admin(db, i.forum_and_admin_id) #for cascade delete
    
    for i in db.query(models.Forum_post).filter(models.Forum_post.forum_id == forum_id).all():
        delete_forum_post(db, i.forum_post_id) #for cascade delete
    



    db_forum = db.query(models.Forum).filter(models.Forum.forum_id == forum_id).first()
    db.delete(db_forum)
    db.commit()
    return db_forum



def get_forum_and_admin(db: Session, forum_and_admin_id: int): #
    return db.query(models.Forum_and_admin).filter(models.Forum_and_admin.forum_and_admin_id == forum_and_admin_id).first()

def get_forums_and_admins(db: Session, skip: int = 0, limit: int = 100): #
    return db.query(models.Forum_and_admin).offset(skip).limit(limit).all()

def create_forum_and_admin(db: Session, forum_and_admin: schemas.Forum_and_adminBase): #
    db_forum_and_admin = models.Forum_and_admin(forum_id=forum_and_admin.forum_id, admin_id = forum_and_admin.admin_id)
    db.add(db_forum_and_admin)
    db.commit()
    #db.refresh(db_forum_and_admin)
    return 0
    return db_forum_and_admin

def update_forum_and_admin(db: Session, forum_and_admin: schemas.Forum_and_adminUpdate): #
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



def get_forum_post(db: Session, forum_post_id: int): #
    return db.query(models.Forum_post).filter(models.Forum_post.forum_post_id == forum_post_id).first()

def get_forum_posts(db: Session, skip: int = 0, limit: int = 100): #
    return db.query(models.Forum_post).offset(skip).limit(limit).all()

def create_forum_post(db: Session, forum_post: schemas.Forum_postCreate): #
    db_forum_post = models.Forum_post(forum_id=forum_post.forum_id, user_id = forum_post.user_id, post_title = forum_post.post_title, post_content = forum_post.post_content)
    db.add(db_forum_post)
    db.commit()
    db.refresh(db_forum_post)
    return db_forum_post

def update_forum_post(db: Session, forum_post: schemas.Forum_postUpdate): #
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
