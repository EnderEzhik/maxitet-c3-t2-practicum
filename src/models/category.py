from typing import List, Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from src.models.links import ModCategoryLink

if TYPE_CHECKING:
    from src.models.mod import Mod


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    category: str = Field(nullable=False, unique=True, index=True)

    mods: List["Mod"] = Relationship(
        link_model=ModCategoryLink,
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class CategoryCreate(SQLModel):
    category: str


class CategoryOut(SQLModel):
    id: int
    category: str


class CategoriesOut(SQLModel):
    data: List[CategoryOut]
    count: int


CategoryOut.model_rebuild()
