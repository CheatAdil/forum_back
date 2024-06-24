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

