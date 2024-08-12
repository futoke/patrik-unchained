import asyncio
from itertools import cycle

from fastapi import FastAPI, WebSocket
# from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse 
from fastapi.staticfiles import StaticFiles


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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    exp_iter = cycle(EXPRESSIONS)
    await websocket.accept()
    while True:
        await websocket.send_text(next(exp_iter))
        await asyncio.sleep(1)