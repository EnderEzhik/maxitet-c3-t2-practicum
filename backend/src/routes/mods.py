from fastapi import APIRouter, HTTPException

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


@router.get("/{mod_id}", response_model=ModOut)
async def get_mod_by_id(session: SessionDep, mod_id: int):
    mod = await mods_repo.get_mod_by_id(session, mod_id)
    if mod is None:
        raise HTTPException(status_code=404, detail="Mod not found")
    return mod


@router.delete("/{mod_id}")
async def delete_mod_by_id(session: SessionDep, mod_id: int):
    ok = await mods_repo.delete_mod_by_id(session, mod_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Mod not found")
    return { "status": "deleted" }
