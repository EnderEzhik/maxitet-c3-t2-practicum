from fastapi import HTTPException

from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.category import Category, CategoryCreate


async def create_category(session: AsyncSession, category_data: CategoryCreate) -> Category:
    category_exists = (await session.exec(select(Category).where(Category.category == category_data.category))).one_or_none()
    if category_exists is not None:
        raise HTTPException(status_code=409, detail=f"Category with name \"{category_data.category}\" already exists")

    category = Category(**category_data.model_dump())
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def get_categories_list(session: AsyncSession) -> tuple[list[Category], int]:
    categories_result = await session.exec(select(Category))
    categories = categories_result.all()

    count_stmt = select(func.count()).select_from(Category)
    count_result = await session.exec(count_stmt)
    count = count_result.one()

    return categories, count


async def get_category(session: AsyncSession, category_name: str) -> Category | None:
    return await session.get(Category, category_name)


async def delete_category(session: AsyncSession, category: str) -> bool:
    category = await get_category(session, category)
    if category is None:
        return False
    await session.delete(category)
    await session.commit()
    return True
