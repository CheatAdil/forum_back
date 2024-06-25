from pydantic import BaseModel

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
