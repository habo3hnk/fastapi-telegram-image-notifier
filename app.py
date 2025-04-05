import logging
import sys
import uvicorn

from fastapi import FastAPI
from api.routers import images
from config.config import HOST, PORT


app = FastAPI()
app.include_router(images.router)

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
