from fastapi import FastAPI

from routers.user_router import user_router
from routers.category_router import category_router
from routers.forum_router import forum_router
from routers.forums_and_admins_router import forums_and_admins_router
from routers.forum_posts_router import forum_posts_router
from routers.token_router import token_router
from websocket.websocket import websocket_chat_router

app = FastAPI()

app.include_router(token_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(forum_router)
app.include_router(forums_and_admins_router)
app.include_router(forum_posts_router)
app.include_router(websocket_chat_router)
