from fastapi import HTTPException

from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.version import Version, VersionCreate


async def create_version(session: AsyncSession, version_data: VersionCreate) -> Version:
    version_exists = (await session.exec(select(Version).where(Version.version == version_data.version))).one_or_none()
    if version_exists is not None:
        raise HTTPException(status_code=409, detail=f"Version with version \"{version_data.version}\" already exists")

    version = Version(**version_data.model_dump())
    session.add(version)
    await session.commit()
    await session.refresh(version)
    return version


async def get_versions_list(session: AsyncSession) -> tuple[list[Version], int]:
    versions_result = await session.exec(select(Version))
    versions = versions_result.all()

    count_stmt = select(func.count()).select_from(Version)
    count_result = await session.exec(count_stmt)
    count = count_result.one()

    return versions, count


async def get_version(session: AsyncSession, version_id: int) -> Version | None:
    return await session.get(Version, version_id)


async def get_version_by_number(session: AsyncSession, version_number: str) -> Version | None:
    return (await session.exec(select(Version).where(Version.version == version_number))).one_or_none()


async def delete_version(session: AsyncSession, version_id: int) -> bool:
    version = await get_version(session, version_id)
    if version is None:
        return False
    await session.delete(version)
    await session.commit()
    return True
