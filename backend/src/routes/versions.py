from fastapi import APIRouter

from src.core.database import SessionDep
from src.models.version import VersionCreate, VersionsOut
import src.repositories.versions as versions_repo


router = APIRouter(prefix="/versions", tags=["Versions"])


@router.post("/")
async def create_version(session: SessionDep, version_data: VersionCreate):
    return await versions_repo.create_version(session, version_data)


@router.get("/", response_model=VersionsOut)
async def get_versions_list(session: SessionDep):
    versions, count = await versions_repo.get_versions_list(session)
    return VersionsOut(data=versions, count=count)
