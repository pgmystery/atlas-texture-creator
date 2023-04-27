from .atlas_collection import AtlasCollection
from .store import AtlasStore
from .types import AtlasManagerConfigType


class AtlasManager:
    def __init__(self, config_path: str):
        self.store = AtlasStore()
        self.load_settings(config_path)

    def load_settings(self, config_path: str):
        # settings = Dynaconf(settings_files=["config.json"], validators=[AtlasManagerConfigType])
        pass

    def new_atlas_collection(self, collection_name: str):
        atlas_collection = AtlasCollection(collection_name)
        self.store.create_collection(atlas_collection)

    def delete_atlas_collection(self, collection_name: str):
        self.store.delete_collection(collection_name)

    def list_atlas_collections(self) -> list[AtlasCollection]:
        return self.store.list_atlas_collections()

    def load_atlas_collection(self):
        pass
