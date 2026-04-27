from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(nullable=False, unique=True, min_length=4, max_length=20)
    hashed_password: str = Field(nullable=False)


class UserCreate(SQLModel):
    username: str = Field(nullable=False, min_length=4, max_length=20)
    password: str = Field(nullable=False, min_length=8, max_length=64)


class UserUpdate(SQLModel):
    username: str | None = Field(min_length=4, max_length=20)
    password: str | None = Field(min_length=8, max_length=64)


class UserOut(SQLModel):
    username: str
