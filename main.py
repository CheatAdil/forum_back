

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware




from .routers.user_router import user_router
from .routers.category_router import category_router
from .routers.forum_router import forum_router
from .routers.forums_and_admins_router import forums_and_admins_router
from .routers.forum_posts_router import forum_posts_router
from .routers.token_router import token_router
from .websocket.websocket import websocket_chat_router

app = FastAPI()

origins = [
    "http://127.0.0.1",
    "https://127.0.0.1",
    "http://127.0.0.1:8000",
    "https://127.0.0.1:8000",
    "http://3.138.247.247",
    "https://3.138.247.247",
    "http://3.138.247.247:8000",
    "https://3.138.247.247:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(token_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(forum_router)
app.include_router(forums_and_admins_router)
app.include_router(forum_posts_router)
app.include_router(websocket_chat_router)





from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://3.138.247.247/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

