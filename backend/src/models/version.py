from sqlmodel import Field, SQLModel, Relationship

from src.models import ModVersions

from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from backend.src.models.mod import Mod


class Version(SQLModel, table=True):
    __tablename__ = "versions"

    version: str = Field(primary_key=True, min_length=3, max_length=10)
    mods: List["Mod"] = Relationship(back_populates="versions", link_model=ModVersions)
