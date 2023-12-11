from typing import Literal, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class AtlasManagerConfigDB(BaseSettings):
    sqlite_path: str = Field("atlas_manager.db")


class AtlasManagerConfig(BaseModel):
    db: Optional[AtlasManagerConfigDB]


AtlasGridDirection = Literal["row", "column"]


Column = int
Row = int


class AtlasGridItem(BaseModel):
    column: Column = -1
    row: Row = -1


class GenerateAtlasOptionsSize(BaseModel):
    width: int
    height: int


class GenerateAtlasOptions(BaseModel):
    lock_size: GenerateAtlasOptionsSize | None


class GenerateAtlasCoordTexture(BaseModel):
    x: int
    y: int
    width: int
    height: int


GenerateAtlasReturnType = dict[str, GenerateAtlasCoordTexture]


class GenerateAtlasReturnTypeOut(BaseModel):
    # __root__: GenerateAtlasReturnType
    pass
