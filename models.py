print(" models")


from SQLAlchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from SQLAlchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer,primary_key=True,nullable=False)
    user_name = Column(String,nullable=False)
    user_password = Column(String,nullable=False)
    user_email = Column(String, nullable=False)
    #registration_date = Column(DateTime(timezone=True), server_default=text('now()'))
    #registration_date = Column(DateTime(timezone=True))

class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer,primary_key=True,nullable=False)
    category_name = Column(String,nullable=False)
    description = Column(String,nullable=False)

    #category_forums = relationship("forum", back_populates="fcategory")

class Forum(Base):
    __tablename__ = "forums"
    forum_id = Column(Integer,primary_key=True,nullable=False)
    forum_name = Column(String,nullable=False)
    forum_category = Column(Integer,ForeignKey("categories.category_id"),nullable=False)
    description = Column(String,nullable=False)

    #fcategory = relationship("category", back_populates="category_forums")

class Forum_and_admin(Base):
    __tablename__ = "forums_and_admins"
    forum_and_admin_id = Column(Integer,primary_key=True,nullable=False)
    forum_id = Column(Integer,ForeignKey("forums.forum_id"),nullable=False)
    admin_id = Column(Integer,ForeignKey("users.user_id"),nullable=False)

class Forum_post(Base):
    __tablename__ = "forum_posts"
    forum_post_id = Column(Integer,primary_key=True,nullable=False)
    forum_id = Column(Integer,ForeignKey("forums.forum_id"),nullable=False)
    user_id = Column(Integer,ForeignKey("users.user_id"),nullable=False)
    post_title = Column(String,nullable=False)
    post_content = Column(String,nullable=False)
    #post_date = Column(DateTime,nullable=False)



