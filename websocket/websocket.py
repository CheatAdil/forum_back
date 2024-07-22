from typing import Annotated

from fastapi import FastAPI, WebSocket, APIRouter, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from ..routers.user_router import read_user_me
from ..entities.schemas import user_schemas
from ..auths.get_current_user import get_current_user

websocket_chat_router = APIRouter(
    prefix="", tags=["chat"]
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Websocket Demo</title>
           <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    </head>
    <body>
    <div class="container mt-3">
        <h1>FastAPI WebSocket Chat</h1>
        <h2>Your name: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" class="form-control" id="messageText" autocomplete="off"/>
            <button class="btn btn-outline-primary mt-2">Send</button>
        </form>
        <ul id='messages' class="mt-5">
        </ul>
        
    </div>
    
        <script>
            function getCookie(cname)
            {
                let name = cname + "=";
                let decodedCookie = decodeURIComponent(document.cookie);
                let ca = decodedCookie.split(';');
                for(let i = 0; i <ca.length; i++)
                {
                    let c = ca[i];
                    while (c.charAt(0) == ' ')
                    {
                        c = c.substring(1);
                    }
                    if (c.indexOf(name) == 0)
                    {
                        return c.substring(name.length, c.length);
                    }
                }
                return "";
            }

            var client_id = httpGet("http://127.0.0.1:8000/me")
            ///var client_id = getCookie("username");
            ///var client_id = 124
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
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
            function httpGet(theUrl)
            {
                var xmlHttp = new XMLHttpRequest();
                xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
                xmlHttp.send( null );
                return xmlHttp.responseText;
            }
            
        </script>
    </body>
</html>
"""

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    
manager = ConnectionManager()


@websocket_chat_router.get("/chat")
async def get():
    return HTMLResponse(html)


@websocket_chat_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try: 
        while True:
            data = await websocket.receive_text()
            #await manager.send_personal_message(f"You wrote: {data} Your id: {read_user_me()}", websocket)
            await manager.broadcast(f"{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{client_id} has left the chat")

@websocket_chat_router.get("/me")
async def read_user_me(current_user: Annotated[user_schemas.User, Depends(get_current_user)]):
    return current_user.user_name
