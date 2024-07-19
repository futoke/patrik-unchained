import os
import sys
import asyncio
import logging
from contextlib import asynccontextmanager

# Set path for script.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
sys.path.append(dname)
os.chdir(dname)

import yaml
from lx16a import LX16A, ServoTimeoutError
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel


queue = asyncio.Queue()
logger = logging.getLogger('uvicorn.error')


class Actions:
    def __init__(self) -> None:
        LX16A.initialize("/dev/ttyUSB0", 0.1)

        with open("config.yml", 'r') as fh:
            config_data = yaml.safe_load(fh)

        logger.info(f"Init servos.")
        self.servos = {}
        self.actions = {}
        for name in config_data["servos"]:
            try:
                self.servos[name] = LX16A(config_data["servos"][name])
            except ServoTimeoutError as ste:
                logger.info(f'Servo "{name}" is not responded.')

        with open("actions.yml", 'r') as fh:
            self.actions = yaml.safe_load(fh)

    def get_all_actions(self) -> list[str]:
        return list(self.actions.keys())

    async def do_action(self, action_name):
        for step in self.actions[action_name]:
            action_time = step["time"]
            positions = step["positions"]

            for servo_id in self.servos:
                self.servos[servo_id].move(positions[servo_id], action_time)

            await asyncio.sleep(action_time / 1000)

actions = Actions()

async def bg_worker():
    while True:
        if not queue.empty():
            action_name = await queue.get()
            await actions.do_action(action_name)
        else:
            await asyncio.sleep(0.1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    bg_task = asyncio.create_task(bg_worker())
    yield
    bg_task.cancel()


app = FastAPI(lifespan=lifespan)


@app.get("/do_action/{action_name}/")
async def do_action(action_name: str):
    logger.info(f"Action '{action_name}' received.")
    await queue.put(action_name)
    return


@app.get("/get-all-actions")
def get_all_actions() -> list[str]:
    return actions.get_all_actions()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)