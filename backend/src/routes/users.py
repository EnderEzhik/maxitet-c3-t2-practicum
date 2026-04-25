from fastapi import APIRouter

from src.core.security import CurrentUserDep
from src.models.user import UserCreate, UserOut
from src.core.database import SessionDep
import src.repositories.users as users_repo


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
async def create_user(
    session: SessionDep,
    user_data: UserCreate
):
    return await users_repo.create_user(session, user_data)


@router.get("/me", response_model=UserOut)
async def read_users_me(
    current_user: CurrentUserDep,
):
    return current_user
