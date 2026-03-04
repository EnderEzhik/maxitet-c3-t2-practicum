from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.mod import Mod, ModCreate, ModUpdate


def _apply_filters(stmt,
                   title: str | None):
    if title:
        title = title.strip()
        if title:
            title = f"%{title}%"
            stmt = stmt.where(Mod.title.ilike(title))
    return stmt


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


async def get_mods_with_filters(
    session: AsyncSession,
    title: str | None = None,
    limit: int = 20,
    offset: int = 0
) -> tuple[list[Mod], int]:
    stmt = select(Mod)
    stmt = _apply_filters(stmt, title)
    stmt = stmt.offset(offset).limit(limit)

    result = await session.exec(stmt)
    mods = result.all()

    count_stmt = select(func.count()).select_from(Mod)
    count_stmt = _apply_filters(count_stmt, title)

    count_result = await session.exec(count_stmt)
    count = count_result.one()

    return mods, count


async def get_mod_by_id(session: AsyncSession, mod_id: UUID) -> Mod | None:
    mod = (await session.exec(select(Mod).where(Mod.id == mod_id))).first()
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
