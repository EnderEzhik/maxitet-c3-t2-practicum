from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.mod import Mod


async def get_mods_list(session: AsyncSession) -> tuple[list[Mod], int]:
    result = await session.exec(select(Mod))
    mods = result.all()

    count_stmt = select(func.count()).select_from(Mod)
    count_result = await session.exec(count_stmt)
    count = count_result.one()

    return mods, count
