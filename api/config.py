from dotenv import load_dotenv
import os

load_dotenv()


TOKEN = str(os.getenv("BOT_TOKEN"))
IMAGE_FOLDER = str(os.getenv("IMAGE_FOLDER"))
