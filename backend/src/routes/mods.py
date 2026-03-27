from fastapi import APIRouter

from src.core.database import SessionDep
from src.models.mod import ModsOut
import src.repositories.mods as mods_repo


router = APIRouter(prefix="/mods", tags=["Mods"])


@router.get("/", response_model=ModsOut)
async def get_all_mods(session: SessionDep):
    mods, count = await mods_repo.get_mods_list(session)
    return ModsOut(data=mods, count=count)
