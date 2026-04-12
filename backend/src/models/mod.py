from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship

from src.models.version import Version, VersionOut
from src.models.category import Category, CategoryOut
from src.models.links import ModVersionLink, ModCategoryLink


class Mod(SQLModel, table=True):
    __tablename__ = "mods"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, min_length=1, max_length=255)
    description: str = Field(nullable=False, min_length=1, max_length=2000)

    versions: List["Version"] = Relationship(
        link_model=ModVersionLink,
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    categories: List["Category"] = Relationship(
        link_model=ModCategoryLink,
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class ModCreate(SQLModel):
    name: str = Field( min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=2000)
    version_ids: List[int] = Field(min_length=1)
    category_ids: List[int] = Field(min_length=1)


class ModOut(SQLModel):
    id: int
    name: str
    description: str
    versions: List[VersionOut]
    categories: List[CategoryOut]


class ModsOut(SQLModel):
    data: List[ModOut]
    count: int


ModOut.model_rebuild()
