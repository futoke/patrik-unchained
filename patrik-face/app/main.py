import asyncio
from typing import Annotated

from fastapi import FastAPI, WebSocket, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.logger import logger

from models import Face, ExpressionsRus, AnimationsRus, EasingRus, EyesRus


app = FastAPI()
app.face = None
app.mount(
    "/static", 
    StaticFiles(directory="app/static/dist", html=True), 
    name="static"
)


@app.get("/")
async def get_main_page():
    return FileResponse('app/index.html')


@app.post("/set_face/")
async def set_face(face: Face):
    app.face = face
    logger.info(face)
    return {"face": face}


@app.get("/get_expressions/")
async def get_expressions():
    expressions = {}
    for exp in ExpressionsRus:
        expressions[exp] = exp.name
    return expressions


@app.get("/get_animations/")
async def get_animations():
    animations = {}
    for anim in AnimationsRus:
        animations[anim] = anim.name
    return animations


@app.get("/get_easing/")
async def get_easing():
    easing = {}
    for ease in EasingRus:
        easing[ease] = ease.name
    return easing


@app.get("/get_eyes/")
async def get_eyes():
    eyes = {}
    for eye in EyesRus:
        eyes[eye] = eye.name
    return eyes


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(1)

        if app.face:
            # await websocket.send_text(app.face.expression.name)
            await websocket.send_json(jsonable_encoder(app.face))