from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import FileResponse
from api.services.image_service import get_image_path

from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import create_image_view, get_image_by_name
from database.dependencies import get_db


router = APIRouter(prefix="/img", tags=["images"])


@router.get("/{image_name}")
async def get_image(
    image_name: str, request: Request, db: AsyncSession = Depends(get_db)
):
    client_ip = request.client.host if request.client else "unknown"
    image = await get_image_by_name(session=db, image_name=image_name)
    if image:
        await create_image_view(
            session=db,
            image_id=image.id,
            ip_address=client_ip,
        )
    image_path = get_image_path(image_name)

    if not image_path:
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path)
