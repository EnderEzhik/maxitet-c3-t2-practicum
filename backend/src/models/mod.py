from typing import List

from sqlmodel import SQLModel, Field


class ModBase(SQLModel):
    title: str = Field(nullable=False, min_length=3, max_length=32)
    description: str = Field(nullable=False, min_length=10, max_length=1000)
    version: str = Field(nullable=False, foreign_key="versions.version")
    category: str = Field(nullable=False, foreign_key="categories.category")


class ModOut(ModBase):
    id: int


class ModsOut(SQLModel):
    data: List[ModOut]
    count: int


class Mod(ModBase, table=True):
    __tablename__ = "mods"

    id: int | None = Field(default=None, primary_key=True)
