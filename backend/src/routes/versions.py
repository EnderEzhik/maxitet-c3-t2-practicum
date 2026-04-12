from fastapi import APIRouter, HTTPException

from src.core.database import SessionDep
from src.models.version import VersionCreate, VersionOut, VersionsOut
import src.repositories.versions as versions_repo


router = APIRouter(prefix="/versions", tags=["Versions"])


@router.post("/")
async def create_version(session: SessionDep, version_data: VersionCreate):
    return await versions_repo.create_version(session, version_data)


@router.get("/", response_model=VersionsOut)
async def get_versions_list(session: SessionDep):
    versions, count = await versions_repo.get_versions_list(session)
    return VersionsOut(data=versions, count=count)


@router.get("/{version}", response_model=VersionOut)
async def get_version(session: SessionDep, version_id: int):
    version = await versions_repo.get_version(session, version_id)
    if version is None:
        raise HTTPException(status_code=404, detail="Version not found")
    return version


@router.delete("/{version}")
async def delete_version(session: SessionDep, version_id: int):
    ok = await versions_repo.delete_version(session, version_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Version not found")
    return { "status": "deleted" }
