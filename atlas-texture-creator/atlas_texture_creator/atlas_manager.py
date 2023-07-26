from .atlas_collection import AtlasCollection
from .store import AtlasStore
from .types import AtlasManagerConfigType


class AtlasManager(AtlasStore):
    def __init__(self, config_path: str = ""):
        super().__init__()
        # self.store = AtlasStore()
        # self.load_settings(config_path)

    # def load_settings(self, config_path: str):
    #     # settings = Dynaconf(settings_files=["config.json"], validators=[AtlasManagerConfigType])
    #     pass

    def create_collection(self, collection_name: str) -> AtlasCollection:
        atlas_collection = AtlasCollection(collection_name)
        super().create_collection(atlas_collection)
        return atlas_collection
    #
    # def delete_atlas_collection(self, collection_name: str):
    #     self.store.delete_collection(collection_name)
    #
    # def list_atlas_collections(self) -> list[AtlasCollection]:
    #     return self.store.list_atlas_collections()
    #
    # def load_atlas_collection(self, collection_name: str) -> AtlasCollection:
    #     return self.store.load_collection(collection_name)
    #
    # def update_atlas_collection(self, collection_name: str, new_collection: AtlasCollection):
    #     self.store.update_collection(collection_name, new_collection)
    #
    # def add_texture_to_collection(self, collection_name: str, texture: AtlasTexture):
    #     self.store.add_texture(collection_name, texture)
