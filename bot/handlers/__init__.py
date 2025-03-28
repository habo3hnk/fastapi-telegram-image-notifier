from aiogram import Router

# from .start import start_router
# from .help import help_router
# from .images import images_router
# from .common import common_router
from .handlers import main_router
from .img_form import img_router


router = Router()

router.include_router(main_router)
router.include_router(img_router)
