from typing import Optional, Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database.models.models import User, Image, ImageView


async def create_user(session: AsyncSession, telegram_id: int) -> User:
    user = User(telegram_id=telegram_id)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_telegram_id(
    session: AsyncSession, telegram_id: int
) -> Optional[User]:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_with_images(
    session: AsyncSession, telegram_id: int
) -> Optional[User]:
    stmt = (
        select(User)
        .where(User.telegram_id == telegram_id)
        .options(selectinload(User.images))
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def delete_user(session: AsyncSession, telegram_id: int) -> bool:
    stmt = delete(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0


async def create_image(
    session: AsyncSession,
    user_id: int,
    file_name: str,
    display_name: Optional[str] = None,
) -> Image:
    image = Image(user_id=user_id, file_name=file_name, display_name=display_name)
    session.add(image)
    await session.commit()
    await session.refresh(image)
    return image


async def get_image_by_id(session: AsyncSession, image_id: int) -> Optional[Image]:
    stmt = select(Image).where(Image.id == image_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_image_by_name(session: AsyncSession, image_name: str) -> Optional[Image]:
    stmt = select(Image).where(Image.file_name == image_name)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_images_by_user(session: AsyncSession, user_id: int) -> Sequence[Image]:
    stmt = select(Image).where(Image.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_user_by_image(session: AsyncSession, image: Image) -> Optional[Image]:
    stmt = select(User).where(Image.id == image.id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_image_display_name(
    session: AsyncSession,
    image_id: int,
    new_display_name: str,
) -> bool:
    stmt = (
        update(Image).where(Image.id == image_id).values(display_name=new_display_name)
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0


async def delete_image(session: AsyncSession, image_id: int) -> bool:
    stmt = delete(Image).where(Image.id == image_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0


async def create_image_view(
    session: AsyncSession,
    image_id: int,
    ip_address: str,
) -> ImageView:
    view = ImageView(image_id=image_id, ip_address=ip_address)
    session.add(view)
    await session.commit()
    await session.refresh(view)
    return view


async def get_views_for_image(
    session: AsyncSession, image_id: int
) -> Sequence[ImageView]:
    stmt = select(ImageView).where(ImageView.image_id == image_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_total_views_count(session: AsyncSession, image_id: int) -> int:
    stmt = select(ImageView).where(ImageView.image_id == image_id)
    result = await session.execute(stmt)
    return len(result.scalars().all())


async def delete_image_view(session: AsyncSession, view_id: int) -> bool:
    stmt = delete(ImageView).where(ImageView.id == view_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
