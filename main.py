from fastapi import FastAPI

from my_package.routers.user_router import user_router
from my_package.routers.category_router import category_router
from my_package.routers.forum_router import forum_router
from my_package.routers.forums_and_admins_router import forums_and_admins_router
from my_package.routers.forum_posts_router import forum_posts_router
from my_package.routers.token_router import token_router

app = FastAPI()

app.include_router(token_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(forum_router)
app.include_router(forums_and_admins_router)
app.include_router(forum_posts_router)