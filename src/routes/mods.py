import aiofiles

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Query, File, UploadFile
from fastapi.responses import FileResponse

from src.core.database import SessionDep
from src.models.mod import ModCreate, ModOut, ModsOut
import src.repositories.mods as mods_repo
import src.repositories.versions as versions_repo


mod_files_dir = Path(__file__).resolve()
mod_files_dir = mod_files_dir.parent.parent.parent
mod_files_dir = mod_files_dir / "mod_files"

router = APIRouter(prefix="/mods", tags=["Mods"])


@router.post("/", response_model=ModOut)
async def create_mod(
    session: SessionDep,
    name: Annotated[str, Form(...)],
    description: Annotated[str, Form(...)],
    version: Annotated[str, Form(...)],
    categories: Annotated[list[str], Form(...)],
    mod_file: Annotated[UploadFile, File(..., description="Версия Minecraft")]
):
    mod_data = ModCreate(name=name, description=description, version=version, categories=categories)
    mod = await mods_repo.create_mod(session, mod_data)

    mod_dir_pth: Path = mod_files_dir / str(mod.id)
    mod_dir_pth.mkdir(parents=True, exist_ok=True)

    mod_file_path: Path = mod_dir_pth / (mod_data.version + ".jar")

    async with aiofiles.open(mod_file_path, "wb") as f:
        content = await mod_file.read()
        await f.write(content)

    return mod


@router.post("/{mod_id}/upload-file", status_code=201)
async def upload_mod_file(session: SessionDep, mod_id: int, mod_file: Annotated[UploadFile, File(...)], version_number: Annotated[str, Query(...)]):
    mod = await mods_repo.get_mod_by_id(session, mod_id)
    if mod is None:
        raise HTTPException(status_code=404, detail="Mod not found")

    version = await versions_repo.get_version_by_number(session, version_number)
    if version is None:
        raise HTTPException(status_code=404, detail="Version not found")

    mod_file_path: Path = mod_files_dir / str(mod.id) / (version_number + ".jar")
    if mod_file_path.exists() or version_number in [v.version for v in mod.versions]:
        raise HTTPException(status_code=404, detail="Mod version already exists")

    async with aiofiles.open(mod_file_path, "wb") as f:
        content = await mod_file.read()
        await f.write(content)

    mod.versions.append(version)
    await session.commit()
    await session.refresh(mod)


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

    mod_file_path: Path = mod_files_dir / str(mod_id) / (version + ".jar")

    if not mod_file_path.exists():
        raise HTTPException(status_code=404, detail="Version not found")

    return FileResponse(
        path=mod_file_path,
        filename=f"{mod.name}_{version}.jar",
    )
