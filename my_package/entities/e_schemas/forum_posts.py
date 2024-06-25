from pydantic import BaseModel

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
        