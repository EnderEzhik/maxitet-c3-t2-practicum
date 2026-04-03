from fastapi import HTTPException

from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.mod import Mod, ModCreate

import src.repositories.versions as versions_repo
import src.repositories.categories as categories_repo


async def create_mod(session: AsyncSession, mod_data: ModCreate) -> Mod:
    version = await versions_repo.get_version(session, mod_data.version)
    if version is None:
        raise HTTPException(status_code=404, detail=f"Version \"{mod_data.version}\" not found")

    category = await categories_repo.get_category(session, mod_data.category)
    if category is None:
        raise HTTPException(status_code=404, detail=f"Category \"{mod_data.category}\" not found")

    mod = Mod(**mod_data.model_dump())
    session.add(mod)
    await session.commit()
    await session.refresh(mod)
    return mod


async def get_mods_list(session: AsyncSession) -> tuple[list[Mod], int]:
    result = await session.exec(select(Mod))
    mods = result.all()

    count_stmt = select(func.count()).select_from(Mod)
    count_result = await session.exec(count_stmt)
    count = count_result.one()

    return mods, count
