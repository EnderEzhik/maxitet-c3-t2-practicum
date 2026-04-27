from fastapi import HTTPException, status

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.user import User, UserCreate, UserUpdate
from src.core.security import verify_password, get_password_hash


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    exists_user = await get_user_by_username(session, user_data.username)
    if exists_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Login already in use")
    user = User(**user_data.model_dump(exclude={"password"}))
    password_hash = get_password_hash(user_data.password)
    user.hashed_password = password_hash

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    return (await session.exec(select(User).where(User.username == username))).one_or_none()


async def authenticate_user(session: AsyncSession, username: str, password: str) -> User | None:
    user = await get_user_by_username(session, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
