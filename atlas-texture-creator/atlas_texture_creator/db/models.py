from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from atlas_texture_creator.atlas_collection import AtlasCollection, AtlasCollectionModel
from atlas_texture_creator.atlas_texture import AtlasTexture


class Collection(AtlasCollection, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    textures: list["Texture"] = Relationship(back_populates="collection")

    def update(self, new_atlas_collection: AtlasCollection):
        new_atlas_collection_model = AtlasCollectionModel(**new_atlas_collection.dict())
        new_atlas_collection_model_dict = dict(new_atlas_collection_model)

        # TODO: NOT WORKING!
        for k, v in self.model_validate(**new_atlas_collection_model_dict).dict(exclude_defaults=True).items():
            setattr(self, k, v)


class Texture(AtlasTexture, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    collection_id: Optional[int] = Field(default=None, foreign_key="collection.id")
    collection: Optional[Collection] = Relationship(back_populates="textures")
    path: str
