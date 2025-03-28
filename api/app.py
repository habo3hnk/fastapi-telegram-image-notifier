import logging
import sys

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

from config import IMAGE_FOLDER

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


app = FastAPI()


@app.get("/img/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join(IMAGE_FOLDER, image_name)

    if os.path.exists(image_path):
        # TODO: add notify
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")
