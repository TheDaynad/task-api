from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from app.shemas.user import UserCreate, UserUpdate, UserPatch, UserResponse
from app.db.database import get_db
from app.CRUD.user import create_user,get_users,get_user,delete_user,update_user,patch_user


user_router = APIRouter()

@user_router.post("/users",response_model=UserResponse)
async def create_user_endpoint(
        user: UserCreate,
        session: AsyncSession = Depends(get_db)
):
    created_user = await create_user(session, user)
    return created_user

@user_router.get("/users",response_model=list[UserResponse])
async def get_users_endpoint(
        session: AsyncSession = Depends(get_db)
):
    users = await get_users(session)
    return users

@user_router.get("/users/{user_id}",response_model=UserResponse)
async def get_user_endpoint(
        user_id: int,
        session: AsyncSession = Depends(get_db)
):
    user = await get_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.delete("/users/{user_id}")
async def delete_user_endpoint(
        user_id: int,
        session: AsyncSession = Depends(get_db)
):
    deleted = await delete_user(session, user_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="User not found")



@user_router.put("/users/{user_id}",response_model=UserResponse)
async def update_user_endpoint(
        user_id: int,
        user_data: UserUpdate,
        session: AsyncSession = Depends(get_db)
):
    updated_user = await update_user(session, user_id, user_data)

    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@user_router.patch("/users/{user_id}",response_model=UserResponse)
async def patch_user_endpoint(
        user_id: int,
        user_data: UserPatch,
        session: AsyncSession = Depends(get_db)
):
    patched_user = await patch_user(session, user_id, user_data)
    if patched_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return patched_user




