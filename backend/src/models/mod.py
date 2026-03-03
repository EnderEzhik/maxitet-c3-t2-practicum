from uuid import UUID, uuid4
from typing import List

from sqlmodel import SQLModel, Field

class ModBase(SQLModel):
    title: str = Field(nullable=False, unique=True, min_length=3, max_length=32)
    description: str = Field(nullable=False, min_length=10, max_length=1000)


class ModCreate(ModBase):
    pass


class ModUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=3, max_length=32)
    description: str | None = Field(default=None, min_length=20, max_length=1000)


class ModOut(ModBase):
    id: UUID


class ModsOut(SQLModel):
    data: List[ModOut]
    count: int


class Mod(ModBase, table=True):
    __tablename__ = "mods"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
