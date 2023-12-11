from typing import overload
from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine, select

from atlas_texture_creator.db.models import Collection, Texture
from atlas_texture_creator.atlas_collection import AtlasCollection
from atlas_texture_creator.atlas_texture import AtlasTexture
from atlas_texture_creator.types import AtlasManagerConfig


class AtlasManager:
    sqlite_file: str = "atlas_manager.db"

    def __init__(self, config: AtlasManagerConfig = None):
        self.config = config
        self._load_config()
        self.db_engine = self._get_db_engine()

    @overload
    def create_collection(self, collection_name: str) -> AtlasCollection: ...

    @overload
    def create_collection(self, atlas_collection: AtlasCollection) -> AtlasCollection: ...

    def create_collection(self, atlas_collection: AtlasCollection | str) -> AtlasCollection:
        if isinstance(atlas_collection, str):
            atlas_collection = AtlasCollection(atlas_collection)

        atlas_collection_model = Collection(name=atlas_collection.name)

        with Session(self.db_engine) as session:
            session.add(atlas_collection_model)
            session.commit()

        return atlas_collection

    def update_collection(self, collection_name: str, new_collection: AtlasCollection) -> AtlasCollection:
        with Session(self.db_engine) as session:
            collection_model = self._load_collection_model(session, collection_name)
            collection_model.update(new_collection)

            session.add(collection_model)
            session.commit()
            session.refresh(collection_model)

            return self.load_collection(collection_model.name)

    def delete_collection(self, collection_name: str):
        with (Session(self.db_engine) as session):
            collection_model = self._load_collection_model(session, collection_name)

            textures_statement = select(Texture).where(Texture.collection_id == collection_model.id)
            texture_models = session.exec(textures_statement)
            for texture_model in texture_models:
                session.delete(texture_model)

            session.delete(collection_model)
            session.commit()

    def list_collections(self) -> list[str]:
        atlas_collections: list[str] = []

        with Session(self.db_engine) as session:
            statement = select(Collection)
            atlas_collection_models = session.exec(statement)

            for atlas_collection_model in atlas_collection_models:
                atlas_collections.append(atlas_collection_model.name)

        return atlas_collections

    def load_collection(self, collection_name: str) -> AtlasCollection | None:
        with Session(self.db_engine) as session:
            collection_model = self._load_collection_model(session, collection_name)

            if collection_model is None:
                return

            collection_name = collection_model.name
            atlas_collection = AtlasCollection(collection_name)

            textures = self.load_textures(collection_name)
            atlas_collection.load_textures(textures)

            return atlas_collection

    def add_texture(self, collection_name: str, texture: AtlasTexture):
        with Session(self.db_engine) as session:
            atlas_collection = self._load_collection_model(session, collection_name)
            texture_model = Texture(
                collection_id=atlas_collection.id,
                path=str(texture.path),
                label=texture.label,
                row=texture.row,
                column=texture.column,
            )

            session.add(texture_model)
            session.commit()

    def load_textures(self, collection_name: str) -> list[AtlasTexture]:
        textures: list[AtlasTexture] = []

        with Session(self.db_engine) as session:
            atlas_collection = self._load_collection_model(session, collection_name)

            for texture_model in atlas_collection.textures:
                texture = AtlasTexture(
                    path=Path(texture_model.path),
                    label=texture_model.label
                )
                texture.set_coord(texture_model.column, texture_model.row)
                textures.append(texture)

        return textures

    def update_texture(self, collection_name: str, texture: AtlasTexture):
        with Session(self.db_engine) as session:
            atlas_collection = self._load_collection_model(session, collection_name)

            statement = select(Texture) \
                .where(Texture.collection_id == atlas_collection.id) \
                .where(Texture.row == texture.row) \
                .where(Texture.column == texture.column)
            texture_model = session.exec(statement).first()

            texture_model.path = str(texture.path)
            texture_model.label = texture.label

            session.add(texture_model)
            session.commit()
            session.refresh(texture_model)

    def close_all_connections(self):
        self.db_engine.dispose()

    @staticmethod
    def _load_collection_model(session: Session, collection_name: str) -> Collection:
        statement = select(Collection).where(Collection.name == collection_name)
        atlas_collection = session.exec(statement).first()

        return atlas_collection

    def _load_config(self):
        if self.config is not None:
            if self.config.db is not None:
                self.sqlite_file = self.config.db.sqlite_path

    def _get_db_engine(self):
        sqlite_url = f"sqlite:///{self.sqlite_file}"
        engine = create_engine(sqlite_url)
        SQLModel.metadata.create_all(engine)
        engine.dispose()

        return engine
