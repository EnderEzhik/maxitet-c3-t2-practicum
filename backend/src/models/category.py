from sqlmodel import Field, SQLModel, Relationship

from src.models import ModCategories

from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from backend.src.models.mod import Mod


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    title: str = Field(primary_key=True, min_length=3, max_length=32)
    mods: List["Mod"] = Relationship(back_populates="categories", link_model=ModCategories)
