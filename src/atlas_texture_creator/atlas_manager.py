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

    def atlas_instances(self):
        pass

    def new_atlas_collection(self, collection_name: str):
        atlas_collection = AtlasCollection(collection_name)
        self.store.create_collection(atlas_collection)

    def load_atlas_collection(self):
        pass
