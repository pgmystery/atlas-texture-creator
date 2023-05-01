from sqlmodel import SQLModel, Session, create_engine, select

from .models import AtlasCollectionModel, AtlasTexturesModel
from ..atlas_collection import AtlasCollection
from ..atlas_texture import AtlasTexture


class AtlasStore:
    def __init__(self):
        sqlite_file_name = "atlas_manager.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = engine = create_engine(sqlite_url)
        SQLModel.metadata.create_all(engine)

    def create_collection(self, atlas_collection: AtlasCollection):
        atlas_collection_model = AtlasCollectionModel(name=atlas_collection.name)
        with Session(self.engine) as session:
            session.add(atlas_collection_model)
            session.commit()

    def update_collection(self, collection_name: str, new_collection: AtlasCollection):
        collection_model = self._load_collection_model(collection_name)
        with Session(self.engine) as session:
            collection_model.name = new_collection.name
            session.add(collection_model)
            session.commit()
            session.refresh(collection_model)

    def delete_collection(self, collection_name: str):
        collection_model = self._load_collection_model(collection_name)

        with Session(self.engine) as session:
            session.delete(collection_model)
            session.commit()

    def list_collections(self) -> list[AtlasCollection]:
        atlas_collections: list[AtlasCollection] = []

        with Session(self.engine) as session:
            statement = select(AtlasCollectionModel)
            atlas_collection_models = session.exec(statement)
            for atlas_collection_model in atlas_collection_models:
                collection_name = atlas_collection_model.name
                atlas_collection = AtlasCollection(collection_name)
                atlas_collections.append(atlas_collection)

        return atlas_collections

    def load_collection(self, collection_name: str) -> AtlasCollection:
        collection_model = self._load_collection_model(collection_name)

        collection_name = collection_model.name
        atlas_collection = AtlasCollection(collection_name)

        textures = self.load_textures(collection_name)
        atlas_collection.load_textures(textures)

        return atlas_collection


    def _load_collection_model(self, collection_name: str) -> AtlasCollectionModel:
        with Session(self.engine) as session:
            statement = select(AtlasCollectionModel).where(AtlasCollectionModel.name == collection_name)
            atlas_collection = session.exec(statement).first()
            return atlas_collection

    def add_texture(self, collection_name: str, texture: AtlasTexture):
        atlas_collection = self._load_collection_model(collection_name)
        texture_model = AtlasTexturesModel(
            collection=atlas_collection.id,
            path=texture.texture_path,
            label=texture.label,
            row=texture.row,
            column=texture.column,
        )
        with Session(self.engine) as session:
            session.add(texture_model)
            session.commit()

    def load_textures(self, collection_name: str) -> list[AtlasTexture]:
        textures: list[AtlasTexture] = []
        atlas_collection = self._load_collection_model(collection_name)

        with Session(self.engine) as session:
            statement = select(AtlasTexturesModel).where(AtlasTexturesModel.collection == atlas_collection.id)
            texture_models = session.exec(statement)

            counter = 0
            for texture_model in texture_models:
                texture = AtlasTexture(
                    id=counter,
                    texture_path=texture_model.path,
                    label=texture_model.label
                )
                texture.set_coord(texture_model.column, texture.row)
                textures.append(texture)
                counter += 1

        return textures

    def update_texture(self, collection_name: str, texture: AtlasTexture):
        atlas_collection = self._load_collection_model(collection_name)

        with Session(self.engine) as session:
            statement = select(AtlasTexturesModel)\
                .where(AtlasTexturesModel.collection == atlas_collection.id) \
                .where(AtlasTexturesModel.row == texture.row) \
                .where(AtlasTexturesModel.column == texture.column)
            texture_model = session.exec(statement).first()

            texture_model.path = texture.texture_path
            texture_model.label = texture.label

            session.add(texture_model)
            session.commit()
            session.refresh(texture_model)
