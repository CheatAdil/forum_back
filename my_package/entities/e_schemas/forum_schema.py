from pydantic import BaseModel

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
