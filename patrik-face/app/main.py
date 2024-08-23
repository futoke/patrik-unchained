import asyncio
from typing import Annotated

from fastapi import FastAPI, WebSocket, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse 
from fastapi.staticfiles import StaticFiles

from models import Face, ExpressionsRus


app = FastAPI()
app.face = None
app.mount("/static", StaticFiles(directory="app/static/dist", html=True), name="static")


@app.get("/")
async def get_main_page():
    return FileResponse('app/index.html')


@app.post("/set_face/")
async def set_face(face: Face):
    app.face = face
    return {"face": face}


@app.get("/get_expressions/")
async def get_expressions():
    expressions = {}

    for exp in ExpressionsRus:
        expressions[exp] = exp.name

    return expressions


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(1)

        if app.face:
            # await websocket.send_text(app.face.expression.name)
            await websocket.send_json(jsonable_encoder(app.face))