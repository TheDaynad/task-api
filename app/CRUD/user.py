
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.shemas.user import UserCreate, UserUpdate,UserPatch
from sqlalchemy import select, delete


async def create_user(session: AsyncSession, user_data : UserCreate):
    user = User(username=user_data.username,
                email=user_data.email,
                is_active=user_data.is_active)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    return user


async def get_users(session: AsyncSession):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


async def delete_user(session: AsyncSession, user_id: int):
    result = await session.execute(
        delete(User).where(User.id == user_id)
    )
    await session.commit()
    return result.rowcount

async def update_user(session: AsyncSession,user_id: int,user_data: UserUpdate):
    user = await get_user(session, user_id)

    if user is None:
        return None

    user.username = user_data.username
    user.email = user_data.email
    user.is_active = user_data.is_active


    await session.commit()
    await session.refresh(user)

    return user

async def patch_user(session: AsyncSession, user_id: int, user_data: UserPatch):
    user = await get_user(session, user_id)

    if user is None:
        return None

    data = user_data.model_dump(exclude_none=True)

    for field, value in data.items():
        setattr(user, field, value)

    await session.commit()
    await session.refresh(user)
    return user







