import io
import os
import sys
import asyncio
import requests
import logging

from contextlib import asynccontextmanager
from pygame import mixer
from fastapi import FastAPI


# Set path for script.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
sys.path.append(dname)
os.chdir(dname)


URL = "http://patrik-tts:8080/say"
PARAMS = {
    "text": "", 
    "voice": "aleksandr", 
    "format": "mp3",
    "volume": 200
}


queue = asyncio.Queue()
logger = logging.getLogger('uvicorn.error')


async def bg_worker():
    mixer.init()
    mixer.music.load("silence.mp3")
    mixer.music.play(-1)

    while True:
        if not queue.empty():
            phrase = await queue.get()

            PARAMS["text"] = phrase
            response = requests.get(URL, params=PARAMS, stream=False)
            if response.status_code == 200:
                phrase_sound = mixer.Sound(io.BytesIO(response.content))
                phrase_sound.play()
            else:
                logger.info(f"TTS error, server code {response.status_code}")
        else:
            await asyncio.sleep(0.01)


@asynccontextmanager
async def lifespan(app: FastAPI):
    bg_task = asyncio.create_task(bg_worker())
    yield
    bg_task.cancel()


app = FastAPI(lifespan=lifespan)


@app.get("/say/{phrase}")
async def say(phrase: str):
    await queue.put(phrase)
    return