import os
import shutil
from pathlib import Path


class CollectionCache(Path):
    def __init__(self, cache_path: Path, collection_name: str):
        super().__init__(cache_path / collection_name)

        self.cache_dir = cache_path
        self.collection_name = collection_name

        self.mkdir(parents=True, exist_ok=True)

    def add_texture(self, texture_file_path: str) -> Path:
        file_name = Path(texture_file_path).name
        file_path = Path(self) / file_name
        shutil.copy(texture_file_path, file_path)

        return file_path

    def replace_texture(self, texture_name: str, new_texture_path: str) -> str:
        os.remove(Path(self) / texture_name)
        new_texture_path = self.add_texture(new_texture_path)

        return str(new_texture_path)

    def delete(self):
        shutil.rmtree(self)


class CollectionCacheHandler:
    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)

    def __call__(self, collection_name: str) -> CollectionCache:
        return CollectionCache(self.cache_dir, collection_name)
