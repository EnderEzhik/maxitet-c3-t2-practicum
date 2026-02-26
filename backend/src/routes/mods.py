from fastapi import APIRouter


router = APIRouter(prefix="/mods")


@router.get("/")
async def get_all_mods():
    raise NotImplementedError()
