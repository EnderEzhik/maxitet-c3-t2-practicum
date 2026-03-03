from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.mod import Mod, ModCreate, ModUpdate


async def create_mod(session: AsyncSession, mod_data: ModCreate) -> Mod:
    mod = Mod(**mod_data.model_dump())
    session.add(mod)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Title is already in use")
    await session.refresh(mod)
    return mod


async def get_all_mods(session: AsyncSession) -> list[Mod]:
    result = await session.exec(select(Mod))
    mods = result.all()
    return mods


async def get_mod_by_id(session: AsyncSession, mod_id: UUID) -> Mod:
    mod = await session.get(Mod, mod_id)
    if mod is None:
        raise HTTPException(status_code=404, detail="Mod not found")
    return mod


async def update_mod(session: AsyncSession, mod_id: UUID, mod_data: ModUpdate) -> Mod:
    mod = await session.get(Mod, mod_id)
    if mod is None:
        raise HTTPException(status_code=404, detail="Mod not found")

    for field, value in mod_data.model_dump(exclude_unset=True).items():
        setattr(mod, field, value)

    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Title is already in use")

    await session.refresh(mod)
    return mod


async def delete_mod(session: AsyncSession, mod_id: UUID) -> None:
    mod = await session.get(Mod, mod_id)
    if mod is None:
        raise HTTPException(status_code=404, detail="Mod not found")

    await session.delete(mod)
    await session.commit()
