from typing import List, Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from src.models.links import ModVersionLink

if TYPE_CHECKING:
    from src.models.mod import Mod


class Version(SQLModel, table=True):
    __tablename__ = "versions"

    id: Optional[int] = Field(default=None, primary_key=True)
    version: str = Field(nullable=False, unique=True, index=True)

    mods: List["Mod"] = Relationship(
        link_model=ModVersionLink,
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class VersionCreate(SQLModel):
    version: str


class VersionOut(SQLModel):
    id: int
    version: str


class VersionsOut(SQLModel):
    data: List[VersionOut]
    count: int


VersionOut.model_rebuild()
