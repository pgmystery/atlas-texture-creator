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
        try:
            shutil.copy(texture_file_path, file_path)
        except shutil.SameFileError:
            pass

        return file_path

    def replace_texture(self, texture_name: str, new_texture_path: str) -> str:
        file_path = Path(self) / texture_name

        if not self._same_file(file_path, Path(new_texture_path)):
            os.remove(file_path)
            new_texture_path = self.add_texture(new_texture_path)

        return str(new_texture_path)

    def delete(self):
        shutil.rmtree(self)

    @staticmethod
    def _same_file(src: Path, dst: Path):
        # Macintosh, Unix.
        if isinstance(src, os.DirEntry) and hasattr(os.path, 'samestat'):
            try:
                return os.path.samestat(src.stat(), os.stat(dst))
            except OSError:
                return False

        if hasattr(os.path, 'samefile'):
            try:
                return os.path.samefile(src, dst)
            except OSError:
                return False

        # All other platforms: check for same pathname.
        return (os.path.normcase(os.path.abspath(src)) ==
                os.path.normcase(os.path.abspath(dst)))


class CollectionCacheHandler:
    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)

    def __call__(self, collection_name: str) -> CollectionCache:
        return CollectionCache(self.cache_dir, collection_name)
