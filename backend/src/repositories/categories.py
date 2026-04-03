from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.category import Category, CategoryCreate


async def create_category(session: AsyncSession, category_data: CategoryCreate) -> Category:
    category = Category(**category_data.model_dump())
    session.add(category)
    await session.commit()
    return category


async def get_categories_list(session: AsyncSession) -> tuple[list[Category], int]:
    result = await session.exec(select(Category))
    categories = result.all()

    count_stmt = select(func.count()).select_from(Category)
    count_result = await session.exec(count_stmt)
    count = count_result.one()

    return categories, count


async def get_category(session: AsyncSession, category: str) -> Category | None:
    return await session.get(Category, category)
