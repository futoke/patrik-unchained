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

from lx16a import LX16A
from fastapi import FastAPI
from fastapi.responses import FileResponse


queue = asyncio.Queue()
logger = logging.getLogger('uvicorn.error')

head_actions = [
    {"time": 1000, "servos": {1:120, 2:25}},
    {"time": 1000, "servos": {1:130, 2:100}},
    {"time": 1000, "servos": {1:140, 2:190}},
    {"time": 1000, "servos": {1:130, 2:100}}
]


class Action:

    def __init__(self) -> None:
        LX16A.initialize("/dev/ttyUSB0", 0.1)

        self.servos = {1: LX16A(1), 2: LX16A(2)}

    async def do_action(self):
        for action in head_actions:
            action_time = action["time"]
            positions = action["servos"]

            # for servo_id in self.servos:
            #     self.servos[servo_id].move(positions[servo_id], action_time)

            await asyncio.sleep(action_time / 1000)



async def bg_worker():
    state = "stop"

    action = Action()

    while True:
        await action.do_action()
        logger.info("NYAA")

    # while True:
    #     if not queue.empty():
    #         state = await queue.get()
    #     if state == "start":
    #         for step in steps:
    #             time = step["time"]
    #             ctrl.move(step["servos"], time=time)
    #             await asyncio.sleep(time / 1000)
    #     if state == "greet":
    #         for greet in greets:
    #             time = greet["time"]
    #             ctrl.move(greet["servos"], time=time)
    #             await asyncio.sleep(time / 1000)
    #     if state == "stop":
    #         await asyncio.sleep(0.1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    bg_task = asyncio.create_task(bg_worker())
    yield
    bg_task.cancel()


app = FastAPI(lifespan=lifespan)
# app = FastAPI()


@app.get("/")
def read_root():
    return FileResponse('index.html')


@app.get("/cmd/{cmd_name}/")
async def do_cmd(cmd_name: str):
    await queue.put(cmd_name)
    return


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

    # ctrl = ServoController(serial.Serial("/dev/ttyUSB0", 115200, timeout=1))

    # while True:
    #     ctrl.move_prepare(1, 400, 500)
    #     ctrl.move_prepare(2, 400, 500)

    #     ctrl.move_start()

    #     time.sleep(0.5)

    #     ctrl.move_prepare(1, 480, 500)
    #     ctrl.move_prepare(2, 480, 500)

    #     ctrl.move_start()

    #     time.sleep(0.5)

    # from lx16a import *

    # LX16A.initialize("/dev/ttyUSB0", 0.1)

    # try:
    #     servo1 = LX16A(1)
    #     servo2 = LX16A(2)
    #     # servo1.set_angle_limits(0, 240)
    #     # servo2.set_angle_limits(0, 240)
    # except ServoTimeoutError as e:
    #     print(f"Servo {e.id_} is not responding. Exiting...")
    #     quit()

    # t = 0
    # while True:
    #     try:
    #         servo1.move(sin(t) * 60 + 100, time=500, wait=True)
    #         servo2.move(cos(t) * 60 + 100, time=500, wait=True)
    #         servo1.move_start()

    #         time.sleep(0.5)
    #         t += 0.1
    #     except ServoArgumentError:
    #         pass
    
    # while True:
    #     try:
    #         servo1.move(120, time=500)
    #         servo2.move(25, time=500)

    #         time.sleep(0.5)

    #         servo1.move(130, time=500)
    #         servo2.move(100, time=500)

    #         time.sleep(0.5)

    #         servo1.move(140, time=500)
    #         servo2.move(190, time=500)

    #         time.sleep(0.5)

    #         servo1.move(130, time=500)
    #         servo2.move(100, time=500)

    #         time.sleep(0.5)
    #     except ServoArgumentError:
    #         pass