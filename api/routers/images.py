import asyncio

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import FileResponse
from api.services.image_service import get_image_path

from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import create_image_view, get_image_by_name, get_user_by_image
from database.dependencies import get_db

from api.services.bot_service import send_notify
from bot.static import static_text

router = APIRouter(prefix="/img", tags=["images"])


@router.get("/{image_name}")
async def get_image(
    image_name: str, request: Request, db: AsyncSession = Depends(get_db)
):
    client_ip = request.client.host if request.client else "unknown"
    image = await get_image_by_name(session=db, image_name=image_name)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    image_path = get_image_path(image_name)
    if not image_path:
        raise HTTPException(status_code=404, detail="Image not found")

    await create_image_view(
        session=db,
        image_id=image.id,
        ip_address=client_ip,
    )
    user = await get_user_by_image(session=db, image=image)
    if user:
        image_name = image.display_name if image.display_name else image.file_name
        text = static_text.notifications["vivied_notification"].format(
            image_name=image_name
        )
        asyncio.create_task(send_notify(chat_id=user.telegram_id, text=text))

    return FileResponse(image_path)
