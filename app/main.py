import os
import asyncio
import logging
from typing import Union
from contextlib import asynccontextmanager

import serial
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .lewansoul_lx16a_controller import ServoController


# Set path for script.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

queue = asyncio.Queue()
logger = logging.getLogger('uvicorn.error')


async def bg_worker():
    serial_port = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
    ctrl = ServoController(serial_port, timeout=5)

    steps = [
        {1:525, 2:688, 3:550, 4:475, 5:762, 6:550, 7:525, 8:688, 9:550, 10:525, 11:762, 12:550, 13:475, 14:688, 15:550, 16:525, 17:762, 18:550},
        {1:525, 2:688, 3:550, 4:475, 5:688, 6:550, 7:525, 8:688, 9:550, 10:525, 11:688, 12:550, 13:475, 14:688, 15:550, 16:525, 17:688, 18:550},
        {1:475, 2:762, 3:550, 4:525, 5:688, 6:550, 7:475, 8:762, 9:550, 10:475, 11:688, 12:550, 13:525, 14:762, 15:550, 16:475, 17:688, 18:550},
        {1:475, 2:688, 3:550, 4:525, 5:688, 6:550, 7:475, 8:688, 9:550, 10:475, 11:688, 12:550, 13:525, 14:688, 15:550, 16:475, 17:688, 18:550}
    ]

    state = "stop"

    while True:
        if not queue.empty():
            state = await queue.get()
        if state == "start":
            for step in steps:
                ctrl.move(step, time=100)
                await asyncio.sleep(0.1)
        if state == "stop":
            await asyncio.sleep(0.1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    bg_task = asyncio.create_task(bg_worker())
    yield
    bg_task.cancel()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return FileResponse('index.html')


@app.get("/cmd/{cmd_name}/")
async def do_cmd(cmd_name: str):
    await queue.put(cmd_name)
    return


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, debug=True)