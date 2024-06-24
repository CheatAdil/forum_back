from pydantic import BaseModel

class UserBase(BaseModel):
    user_name: str

class UserCreate(UserBase):
    user_password: str
    user_email: str

class UserUpdate(UserCreate):
    user_id: int

class User(UserBase):
    user_id: int
    user_password: str
    user_email: str
    #user_registry_date: time.struct_time

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    category_name: str
class CategoryCreate(CategoryBase):
    description: str
class CategoryUpdate(CategoryCreate):
    category_id: int
class Category(CategoryBase):
    category_id: int
    description: str

    class Config:
        orm_mode = True


class ForumBase(BaseModel):
    forum_name: str
class ForumCreate(ForumBase):
    forum_category: int
    description:str
class ForumUpdate(ForumCreate):
    forum_id: int
class Forum(ForumBase):
    forum_id: int
    forum_category: int
    description: str
    class Config:
        orm_mode = True


class Forum_and_adminBase(BaseModel):
    forum_id: int
    admin_id: int
class Forum_and_adminUpdate(Forum_and_adminBase):
    forum_and_admin_id: int
class Forum_and_admin(Forum_and_adminBase):
    forum_and_admin_id: int
    class Config:
        orm_mode = True


class Forum_postBase(BaseModel):
    forum_id: int
    user_id: int
class Forum_postCreate(Forum_postBase):
    post_title: str
    post_content: str
class Forum_postUpdate(Forum_postCreate):
    forum_post_id: int
class Forum_post(Forum_postBase):
    post_id: int
    post_title: str
    post_content: str

    class Config:
        orm_mode = True