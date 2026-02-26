from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mod import Mod
    from .version import Version
    from .category import Category

__all__ = ["Mod", "Version", "Category"]


from uuid import UUID

from sqlmodel import SQLModel, Field


class ModCategories(SQLModel, table=True):
    mod_id: UUID = Field(foreign_key="mods.id", primary_key=True)
    category_id: str = Field(foreign_key="categories.title", primary_key=True)


class ModVersions(SQLModel, table=True):
    mod_id: UUID = Field(foreign_key="mods.id", primary_key=True)
    version_id: str = Field(foreign_key="versions.version", primary_key=True)
