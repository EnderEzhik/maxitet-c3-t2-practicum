from fastapi import APIRouter

from src.core.database import SessionDep
from src.models.category import CategoryCreate, CategoriesOut
import src.repositories.categories as categories_repo


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/")
async def create_category(session: SessionDep, category_data: CategoryCreate):
    return await categories_repo.create_category(session, category_data)


@router.get("/", response_model=CategoriesOut)
async def get_categories_list(session: SessionDep):
    categories, count = await categories_repo.get_categories_list(session)
    return CategoriesOut(data=categories, count=count)
