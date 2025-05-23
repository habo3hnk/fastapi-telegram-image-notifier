from dotenv import load_dotenv
import os

load_dotenv()


HOST = str(os.getenv("HOST", "127.0.0.1"))
PORT = int(os.getenv("PORT", 8000))

TOKEN = str(os.getenv("BOT_TOKEN"))
IMAGE_FOLDER = str(os.getenv("IMAGE_FOLDER"))
SERVER_URL = str(os.getenv("SERVER_URL"))
IMG_MAX_SIZE_MB = int(os.getenv("IMG_MAX_SIZE_MB", default=5))

DATABASE_URL = str(os.getenv("DATABASE_URL"))


if IMAGE_FOLDER:
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
