from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.core.database import SessionDep
from src.models.mod import ModCreate, ModUpdate, ModOut, ModsOut
import src.repositories.mods as mods_repo


router = APIRouter(prefix="/mods")


@router.post("/", response_model=ModOut)
async def create_mod(session: SessionDep, mod_data: ModCreate):
    mod = await mods_repo.create_mod(session, mod_data)
    return mod


@router.get("/", response_model=ModsOut)
async def get_all_mods(session: SessionDep, title: str | None = None):
    mods, count = await mods_repo.get_mods_with_filters(session, title)
    return ModsOut(data=mods, count=count)


@router.get("/{mod_id}", response_model=ModOut)
async def get_mod_by_id(session: SessionDep, mod_id: UUID):
    mod = await mods_repo.get_mod_by_id(session, mod_id)
    if mod is None:
        raise HTTPException(status_code=404, detail="Mod not found")
    return mod


@router.patch("/{mod_id}", response_model=ModOut)
async def update_mod(session: SessionDep, mod_id: UUID, mod_data: ModUpdate):
    mod = await mods_repo.update_mod(session, mod_id, mod_data)
    return mod


@router.delete("/{mod_id}", status_code=204)
async def delete_mod(session: SessionDep, mod_id: UUID):
    await mods_repo.delete_mod(session, mod_id)
