import os
from config.config import IMAGE_FOLDER


def get_image_path(image_name: str) -> str | None:
    image_path = os.path.join(IMAGE_FOLDER, image_name)
    return image_path if os.path.exists(image_path) else None
