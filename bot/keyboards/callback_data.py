from enum import Enum


class CallbackData(Enum):
    CREATE_IMAGE = "NEW_IMG"
    GET_IMG_LIST = "GET_IMG_LIST"
    CANCEL = "CANCEL"
