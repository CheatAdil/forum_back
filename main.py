
print("main 1")
print("main 0")
print("main 10")


from sqlalchemy.orm import Session
print("main 1.2")


from my_package import database

print("main 1.3")


from database import SessionLocal, engine
print("main 1.31")
from my_package import models

print("main 1.32")

from my_package import schemas
print("main 1.33")
from my_package import crud

print("main 1.4")

print("main 1.5")
models.Base.metadata.create_all(bind=engine)

print("main 2")

#



from . import auth
from .auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user

from datetime import timedelta
from typing import Annotated


from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm




##

print("main 3")

app = FastAPI()

print("print")
'''

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db),
) -> auth.Token:
    db_user = crud.get_user_by_email(db, user_email=form_data.username)
    user = authenticate_user(db_user, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user_name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_email}, expires_delta=access_token_expires
    )
    return auth.Token(access_token=access_token, token_type="bearer")


@app.get("/users/{user_email}", response_model=schemas.User)
def check_user(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    return current_user

@app.post("/users/", response_model=schemas.User)
def create_user(current_user: Annotated[schemas.User, Depends(get_current_user)], user: schemas.UserCreate, db: Session = Depends(get_db) ):

    db_user = crud.get_user_by_email(db, user_email=user.user_email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


#this one
@app.get("/users/", response_model=list[schemas.User])
def read_users(current_user: Annotated[schemas.User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(current_user: Annotated[schemas.User, Depends(get_current_user)], user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(current_user: Annotated[schemas.User, Depends(get_current_user)], user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user.user_email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.update_user(db=db, user=user)

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(current_user: Annotated[schemas.User, Depends(get_current_user)], user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    #if db_user is None:
    #    raise HTTPException(status_code=404, detail="User not found")
    return db_user




@app.post("/categories/", response_model=schemas.Category)
def create_category(current_user: Annotated[schemas.User, Depends(get_current_user)], category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, category_name=category.category_name)
    if db_category:
        raise HTTPException(status_code=400, detail="category already registered")
    return crud.create_category(db=db, category=category)

@app.get("/categories/", response_model=list[schemas.Category])
def read_categorys(current_user: Annotated[schemas.User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categorys(db, skip=skip, limit=limit)
    return categories

@app.get("/categories/{category_id}", response_model=schemas.Category)
def read_category(current_user: Annotated[schemas.User, Depends(get_current_user)], category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.put("/categories/{category_id}", response_model=schemas.Category)
def update_category(current_user: Annotated[schemas.User, Depends(get_current_user)], category: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, category_name=category.category_name)
    #if db_category:
        #raise HTTPException(status_code=400, detail="Email already registered")
    return crud.update_category(db=db, category=category)

@app.delete("/categories/{category_id}", response_model=schemas.Category)
def delete_category(current_user: Annotated[schemas.User, Depends(get_current_user)], category_id: int, db: Session = Depends(get_db)):
    db_category = crud.delete_category(db, category_id=category_id)
    #if db_category is None:
    #    raise HTTPException(status_code=404, detail="Category not found")
    return db_category



@app.post("/forums/", response_model=schemas.Forum)
def create_forum(current_user: Annotated[schemas.User, Depends(get_current_user)], forum: schemas.ForumCreate, db: Session = Depends(get_db)):
    db_forum = crud.get_forum_by_name(db, forum_name=forum.forum_name)
    if db_forum:
        raise HTTPException(status_code=400, detail="forum already registered")
    return crud.create_forum(db=db, forum=forum)

@app.get("/forums/", response_model=list[schemas.Forum])
def read_forums(current_user: Annotated[schemas.User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    forums = crud.get_forums(db, skip=skip, limit=limit)
    return forums

@app.get("/forums/{forum_id}", response_model=schemas.Forum)
def read_forum(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_id: int, db: Session = Depends(get_db)):
    db_forum = crud.get_forum(db, forum_id=forum_id)
    if db_forum is None:
        raise HTTPException(status_code=404, detail="Forum not found")
    return db_forum

@app.put("/forums/{forum_id}", response_model=schemas.Forum)
def update_forum(current_user: Annotated[schemas.User, Depends(get_current_user)], forum: schemas.ForumUpdate, db: Session = Depends(get_db)):
    db_forum = crud.get_forum_by_name(db, forum_name=forum.forum_name)
    #if db_forum:
        #raise HTTPException(status_code=400, detail="Email already registered")
    return crud.update_forum(db=db, forum=forum)

@app.delete("/forums/{forum_id}", response_model=schemas.Forum)
def delete_forum(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_id: int, db: Session = Depends(get_db)):
    db_forum = crud.delete_forum(db, forum_id=forum_id)
    #if db_forum is None:
    #    raise HTTPException(status_code=404, detail="Forum not found")
    return db_forum



@app.post("/forums_and_admins/", response_model=schemas.Forum_and_adminBase)
def create_forum_and_admin(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_and_admin: schemas.Forum_and_adminBase, db: Session = Depends(get_db)):
    crud.create_forum_and_admin(db=db, forum_and_admin=forum_and_admin)
    return 0

@app.get("/forums_and_admins/", response_model=list[schemas.Forum_and_adminBase])
def read_forums_and_admins(current_user: Annotated[schemas.User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    forums = crud.get_forums_and_admins(db, skip=skip, limit=limit)
    return forums


@app.get("/forum_and_admin/{forum_and_admin_id}", response_model=schemas.Forum_and_admin)
def read_forum_and_admin(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_and_admin_id: int, db: Session = Depends(get_db)):
    db_forum_and_admin = crud.get_forum_and_admin(db, forum_and_admin_id=forum_and_admin_id)
    if db_forum_and_admin is None:
        raise HTTPException(status_code=404, detail="Forum_and_admin not found")
    return db_forum_and_admin

@app.put("/forums_and_admins/{forum_and_admin_id}", response_model=schemas.Forum_and_admin)
def update_forum_and_admin(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_and_admin: schemas.Forum_and_adminUpdate, db: Session = Depends(get_db)):
    db_forum_and_admin = crud.get_forum_and_admin(db, forum_and_admin_id=forum_and_admin.forum_and_admin_id)
    return crud.update_forum_and_admin(db=db, forum_and_admin=forum_and_admin)

@app.delete("/forums_and_admins/{forum_and_admin_id}", response_model=schemas.Forum_and_admin)
def delete_forum_and_admin(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_and_admin_id: int, db: Session = Depends(get_db)):
    db_forum_and_admin = crud.delete_forum_and_admin(db, forum_and_admin_id=forum_and_admin_id)
    return db_forum_and_admin



@app.post("/forum_posts/", response_model=schemas.Forum_postCreate)
def create_forum_post(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_post: schemas.Forum_postCreate, db: Session = Depends(get_db)):
    crud.create_forum_post(db=db, forum_post=forum_post)
    return 0

@app.get("/forum_posts/", response_model=list[schemas.Forum_post])
def read_forum_posts(current_user: Annotated[schemas.User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    forums = crud.get_forum_posts(db, skip=skip, limit=limit)
    return forums


@app.get("/forum_post/{forum_post_id}", response_model=schemas.Forum_post)
def read_forum_post(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_post_id: int, db: Session = Depends(get_db)):
    db_forum_post = crud.get_forum_post(db, forum_post_id=forum_post_id)
    if db_forum_post is None:
        raise HTTPException(status_code=404, detail="Forum_post not found")
    return db_forum_post

@app.put("/forum_posts/{forum_post_id}", response_model=schemas.Forum_post)
def update_forum_post(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_post: schemas.Forum_postUpdate, db: Session = Depends(get_db)):
    db_forum_post = crud.get_forum_post(db, forum_post_id=forum_post.forum_post_id)
    return crud.update_forum_post(db=db, forum_post=forum_post)

@app.delete("/forum_posts/{forum_post_id}", response_model=schemas.Forum_post)
def delete_forum_post(current_user: Annotated[schemas.User, Depends(get_current_user)], forum_post_id: int, db: Session = Depends(get_db)):
    db_forum_post = crud.delete_forum_post(db, forum_post_id=forum_post_id)
    return db_forum_post

'''