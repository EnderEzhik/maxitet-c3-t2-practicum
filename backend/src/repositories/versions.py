from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.version import Version, VersionCreate


async def create_version(session: AsyncSession, version_data: VersionCreate) -> Version:
    version = Version(**version_data.model_dump())
    session.add(version)
    await session.commit()
    return version


async def get_versions_list(session: AsyncSession) -> tuple[list[Version], int]:
    result = await session.exec(select(Version))
    versions = result.all()

    count_stmt = select(func.count()).select_from(Version)
    count_result = await session.exec(count_stmt)
    count = count_result.one()

    return versions, count


async def get_version(session: AsyncSession, version: str) -> Version | None:
    return await session.get(Version, version)
