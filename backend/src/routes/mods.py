from fastapi import APIRouter

from src.core.database import SessionDep
from src.models.mod import ModCreate, ModOut, ModsOut
import src.repositories.mods as mods_repo


router = APIRouter(prefix="/mods", tags=["Mods"])


@router.post("/")
async def create_mod(session: SessionDep, mod_data: ModCreate):
    return await mods_repo.create_mod(session, mod_data)


@router.get("/", response_model=ModsOut)
async def get_mods_list(session: SessionDep):
    mods, count = await mods_repo.get_mods_list(session)
    return ModsOut(data=mods, count=count)
