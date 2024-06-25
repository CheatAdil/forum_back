from pydantic import BaseModel

class Forum_and_adminBase(BaseModel):
    forum_id: int
    admin_id: int
class Forum_and_adminUpdate(Forum_and_adminBase):
    forum_and_admin_id: int
class Forum_and_admin(Forum_and_adminBase):
    forum_and_admin_id: int
    class Config:
        orm_mode = True
