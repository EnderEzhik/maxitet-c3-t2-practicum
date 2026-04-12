from fastapi import HTTPException
from sqlalchemy import and_

from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.links import ModCategoryLink, ModVersionLink
from src.models.version import Version
from src.models.category import Category
from src.models.mod import Mod, ModCreate


async def create_mod(session: AsyncSession, mod_data: ModCreate) -> Mod:
    mod_exists = (await session.exec(select(Mod).where(Mod.name == mod_data.name))).one_or_none()
    if mod_exists is not None:
        raise HTTPException(status_code=409, detail=f"Mod with name \"{mod_data.name}\" already exists")

    mod = Mod(**mod_data.model_dump(exclude={"version_ids"}))

    versions_stmt = select(Version).where(Version.id.in_(mod_data.version_ids))
    versions_result = await session.exec(versions_stmt)
    versions = list(versions_result.all())
    if len(versions) != len(mod_data.version_ids):
        raise HTTPException(
            status_code=404,
            detail="One or more Minecraft versions not found"
        )

    mod.versions = versions

    categories_stmt = select(Category).where(Category.id.in_(mod_data.category_ids))
    categories_result = await session.exec(categories_stmt)
    categories = list(categories_result.all())
    if len(categories) != len(mod_data.category_ids):
        raise HTTPException(
            status_code=404,
            detail="One or more categories not found"
        )

    mod.categories = categories

    session.add(mod)
    await session.commit()
    await session.refresh(mod)
    return mod


async def get_mods_list(
    session: AsyncSession,
    title: str | None = None,
    version_id: int | None = None,
    categories: list[str] | None = None,
) -> tuple[list[Mod], int]:
    conditions = []

    if title and title.strip():
        conditions.append(Mod.name.ilike(f"%{title.strip()}%"))

    if version_id is not None:
        version_mod_ids = select(ModVersionLink.mod_id).where(
            ModVersionLink.version_id == version_id
        )
        conditions.append(Mod.id.in_(version_mod_ids))

    if categories:
        category_mod_ids = (
            select(ModCategoryLink.mod_id)
            .join(Category, Category.id == ModCategoryLink.category_id)
            .where(Category.category.in_(categories))
        )
        conditions.append(Mod.id.in_(category_mod_ids))

    stmt = select(Mod)
    count_stmt = select(func.count()).select_from(Mod)
    if conditions:
        where_clause = and_(*conditions)
        stmt = stmt.where(where_clause)
        count_stmt = count_stmt.where(where_clause)

    result = await session.exec(stmt)
    mods = list(result.all())

    count_result = await session.exec(count_stmt)
    count = count_result.one()

    return mods, count


async def get_mod_by_id(session: AsyncSession, mod_id: int) -> Mod | None:
    return await session.get(Mod, mod_id)


async def delete_mod_by_id(session: AsyncSession, mod_id: int) -> bool:
    mod = await get_mod_by_id(session, mod_id)
    if mod is None:
        return False
    await session.delete(mod)
    await session.commit()
    return True
