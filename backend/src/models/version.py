from typing import List

from sqlmodel import SQLModel, Field


class VersionBase(SQLModel):
    version: str = Field(primary_key=True)


class VersionOut(VersionBase):
    pass


class VersionsOut(SQLModel):
    data: List[VersionOut]
    count: int


class Version(VersionBase, table=True):
    __tablename__ = "versions"
