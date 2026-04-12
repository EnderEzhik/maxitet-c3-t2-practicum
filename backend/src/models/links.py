from sqlmodel import SQLModel, Field


class ModVersionLink(SQLModel, table=True):
    __tablename__ = "mod_version_links"

    mod_id: int = Field(foreign_key="mods.id", primary_key=True)
    version_id: int = Field(foreign_key="versions.id", primary_key=True)


class ModCategoryLink(SQLModel, table=True):
    __tablename__ = "mod_category_links"

    mod_id: int = Field(foreign_key="mods.id", primary_key=True)
    category_id: int = Field(foreign_key="categories.id", primary_key=True)
