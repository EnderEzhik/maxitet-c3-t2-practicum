from typing import List

from sqlmodel import SQLModel, Field


class CategoryBase(SQLModel):
    category: str = Field(primary_key=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    pass


class CategoriesOut(SQLModel):
    data: List[CategoryOut]
    count: int


class Category(CategoryBase, table=True):
    __tablename__ = "categories"
