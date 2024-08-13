import asyncio
from itertools import cycle
from dataclasses import dataclass

from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse 
from fastapi.staticfiles import StaticFiles

from models import ModelExpression


@dataclass
class Face:
    expression: str = "default"


EXPRESSIONS = [
    "annoyed", "anxious", "apologetic", "awkward", "blinking", "bored",
    "crying", "default", "determined", "embarrased", "evil", "excited", 
    "exhausted", "flustered", "furious", "giggle", "happy", "in-love",
    "mischievous", "realized-something", "sad", "sassy", "scared", "shocked",
    "snoozing", "starstruck", "stuck-up", "thinking", "tired", "upset",
    "winking", "wow"
]

app = FastAPI()
app.mount("/static", StaticFiles(directory="static/dist", html=True), name="static")

face = Face()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <label id="lbl"></label>

        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");

            function createRandomString(length) {
                const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
                let result = "";

                for (let i = 0; i < length; i++) {
                    result += chars.charAt(Math.floor(Math.random() * chars.length));
                }
                return result;
            }
            
            ws.onmessage = function(event) {
                let labelElement = document.getElementById("lbl");
                labelElement.innerText = createRandomString(16);
            };
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return FileResponse('index.html')


@app.get("/expression/{expression}")
async def set_expression(expression: ModelExpression):
    face.expression = expression
    
    return {"expression": expression}



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_text(face.expression)
        await asyncio.sleep(1)