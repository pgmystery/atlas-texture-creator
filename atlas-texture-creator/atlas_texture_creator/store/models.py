from typing import Optional
from sqlmodel import SQLModel, Field


class AtlasCollectionModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)


class AtlasTexturesModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path: str
    label: str
    row: int
    column: int
    collection: int = Field(foreign_key="atlascollectionmodel.id")
