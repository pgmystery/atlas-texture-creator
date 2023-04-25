# from dynaconf import Dynaconf

from .types import AtlasManagerConfigType


class AtlasManager:
    def __init__(self, config_path: str):
        self.load_settings(config_path)

    def load_settings(self, config_path: str):
        # settings = Dynaconf(settings_files=["config.json"], validators=[AtlasManagerConfigType])
        pass

    def atlas_instances(self):
        pass

    def new_atlas_collection(self):
        pass

    def load_atlas_collection(self):
        pass
