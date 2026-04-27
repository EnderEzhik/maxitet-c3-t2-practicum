import aiofiles

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Query, File, UploadFile
from fastapi.responses import FileResponse

from src.core.database import SessionDep
from src.models.mod import ModCreate, ModOut, ModsOut
import src.repositories.mods as mods_repo


mod_files_dir = Path(__file__).resolve().parents[1] / "mod_files"

router = APIRouter(prefix="/mods", tags=["Mods"])


@router.post("/", response_model=ModOut)
async def create_mod(
    session: SessionDep,
    title: str = Form(...),
    description: str = Form(...),
    version_id: int = Form(...),
    category_id: int = Form(...),
    file: UploadFile = File(...)
):
    mod_data = ModCreate(
        name=title,
        description=description,
        version_id=version_id,
        category_id=category_id
    )

    mod = await mods_repo.create_mod(session, mod_data)
    mod_file_path = mod_files_dir / str(mod.id) / mod_data.version_id

    async with aiofiles.open(mod_file_path, "wb") as f:
        content = await file.read()
        await f.write(content)
    return mod


@router.get("/", response_model=ModsOut)
async def get_mods_list(
    session: SessionDep,
    title: str | None = Query(
        default=None,
        description="Подстрока в названии мода (без учёта регистра)",
    ),
    version_id: int | None = Query(
        default=None,
        description="ID версии Minecraft; вернутся моды, у которых есть эта версия",
    ),
    categories: Annotated[
        list[str] | None,
        Query(description="Имена категорий; мод должен иметь хотя бы одну из них"),
    ] = None,
):
    mods, count = await mods_repo.get_mods_list(session, title, version_id, categories)
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


@router.get("/{mod_id}/download")
async def download_mod_by_id(
    session: SessionDep,
    mod_id: int,
    version: str = Query(description="Версия майнкрафт"),
):
    mod = await mods_repo.get_mod_by_id(session, mod_id)
    if mod is None:
        raise HTTPException(status_code=404, detail="Mod not found")

    mod_file_path = mod_files_dir / str(mod_id) / version

    if not mod_file_path.is_file():
        raise HTTPException(status_code=500, detail="Server error")

    return FileResponse(
        path=mod_file_path,
        filename=f"{mod.name}_{version}",
    )
