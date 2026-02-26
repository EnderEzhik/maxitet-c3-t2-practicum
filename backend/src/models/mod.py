from uuid import UUID, uuid4
from typing import  TYPE_CHECKING, List

from sqlmodel import Relationship, SQLModel, Field

from src.models import ModCategories, ModVersions

if TYPE_CHECKING:
    from backend.src.models.version import Version
    from backend.src.models.category import Category
    from backend.src.models.version import Version


class ModBase(SQLModel):
    title: str = Field(nullable=False, unique=True, min_length=3, max_length=32)
    description: str = Field(nullable=False, min_length=20, max_length=1000)
    author: str = Field(nullable=False, min_length=3, max_length=32)
    # categories: list["Category"] = Field(nullable=False)
    # versions: list["Version"] = Field(nullable=False)


class ModCreate(ModBase):
    pass


class ModUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=3, max_length=32)
    description: str | None = Field(default=None, min_length=20, max_length=1000)
    author: str | None = Field(default=None, min_length=3, max_length=32)
    categories: list["Category"] | None = Field(default=None)
    versions: list["Version"] | None = Field(default=None)


class ModOut(ModBase):
    id: UUID
    rating: float


class ModsOut(SQLModel):
    data: list[ModOut]
    count: int


class Mod(ModBase, table=True):
    __tablename__ = "mods"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    rating: float = Field(default=None, ge=0.0, le=5.0)
    categories: List["Category"] = Relationship(back_populates="mods", link_model=ModCategories)
    versions: List["Version"] = Relationship(back_populates="mods", link_model=ModVersions)
