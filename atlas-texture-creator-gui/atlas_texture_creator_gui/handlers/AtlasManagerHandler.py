import os
import shutil
from pathlib import Path
from typing import overload
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QInputDialog, QApplication, QMessageBox, QFileDialog

from atlas_texture_creator import AtlasManager, AtlasCollection, AtlasTexture
from atlas_texture_creator_gui.Window.GenerateAtlasWindow import GenerateAtlasWindow, GenerateAtlasReturnType
from atlas_texture_creator_gui.handlers.CollectionCacheHandler import CollectionCacheHandler


class AtlasManagerHandler(QObject):
    on_load_collections = Signal(list)
    on_current_collection_changed = Signal(AtlasCollection)
    on_collection_created = Signal(AtlasCollection)
    on_collection_deleted = Signal(str)
    on_textures_added = Signal(AtlasCollection, list)

    def __init__(self, app: QApplication, cache_dir: str):
        super().__init__(app)
        self.app = app
        self.atlas_manager = AtlasManager()
        self._current_collection: AtlasCollection | None = None

        self._collection_cache_handler = CollectionCacheHandler(cache_dir)

    def load_collections(self):
        collections = self.collections()
        self.on_load_collections.emit(collections)

        if len(collections) > 0 and self.current_collection is None:
            self.current_collection = collections[0]

    def collections(self):
        return self.atlas_manager.list_collections()

    @overload
    def current_collection(self, collection: AtlasCollection): ...

    @overload
    def current_collection(self, collection_name: str): ...

    @overload
    def current_collection(self, collection_name: None): ...

    @property
    def current_collection(self):
        return self._current_collection

    @current_collection.setter
    def current_collection(self, collection: AtlasCollection | str | None):
        if collection is None:
            collections = self.atlas_manager.list_collections()
            if len(collections) > 0:
                self._current_collection = collections[0]
            else:
                self._current_collection = None
        elif isinstance(collection, AtlasCollection):
            if self._current_collection == collection.name:
                return

            self._current_collection = collection
        elif isinstance(collection, str):
            if self._current_collection == collection:
                return

            collection = self.atlas_manager.load_collection(collection)
            self._current_collection = collection
        else:
            raise TypeError("Bad collection type")

        self.on_current_collection_changed.emit(collection)

    def create_collection(self) -> AtlasCollection | None:
        collection_name, is_ok = QInputDialog.getText(
            self.app.activeWindow(),
            "Create Atlas-Collection",
            "Enter your new Atlas-Collection name"
        )

        if is_ok:
            atlas_collection = self.atlas_manager.create_collection(collection_name)
            self.on_collection_created.emit(atlas_collection)
            self.current_collection = atlas_collection

            return atlas_collection

    def delete_collection(self, collection_name: str):
        answer = QMessageBox.question(
            self.app.activeWindow(),
            "Delete Collection?",
            f"Do you really want to delete the collection '{collection_name}'?"
            f"\nAll attached textures also getting deleted!",
            QMessageBox.Yes | QMessageBox.No
        )
        if answer == QMessageBox.Yes:
            self.atlas_manager.delete_collection(collection_name)
            cache_collection = self._collection_cache_handler(collection_name)
            cache_collection.delete()
            self.on_collection_deleted.emit(collection_name)

            if self.current_collection is not None and self.current_collection.name == collection_name:
                self.current_collection = None

    def delete_current_collection(self):
        self.delete_collection(self.current_collection.name)

    def generate_current_collection_to_atlas(self):
        if self.current_collection is not None:
            self.generate_atlas(self.current_collection)

    @overload
    def generate_atlas(self, collection: AtlasCollection): ...

    @overload
    def generate_atlas(self, collection: str): ...

    def generate_atlas(self, collection: AtlasCollection | str):
        def generate_atlas_callback(options: GenerateAtlasReturnType):
            save_path = options.file_path
            save_path_dir = os.path.dirname(save_path)
            save_path_obj = Path(save_path)
            texture_coords_path = os.path.join(save_path_dir, f"{save_path_obj.stem}.json")

            img, texture_coords = collection.generate_atlas(options)

            img.save(save_path)
            with open(texture_coords_path, 'w') as f:
                f.write(texture_coords.json())

        if isinstance(collection, str):
            collection = self.atlas_manager.load_collection(collection)
        elif not isinstance(collection, AtlasCollection):
            raise TypeError("Bad collection type")

        self.generate_atlas_window = GenerateAtlasWindow(generate_atlas_callback)
        self.generate_atlas_window.show()

    def add_texture_to_current_collection(self):
        if self.current_collection is not None:
            self.add_texture_to_collection(self.current_collection)

    def add_texture_to_collection(self, collection: AtlasCollection):
        window = self.app.activeWindow()
        texture_open_dialog = QFileDialog(window)
        texture_open_dialog_images_filter = "Images (*.png *.jpg)"

        file_paths = texture_open_dialog.getOpenFileNames(
            window,
            "Select the texture to add",
            "",
            texture_open_dialog_images_filter,
            texture_open_dialog_images_filter
        )[0]

        if len(file_paths) > 0:
            atlas_textures = []
            cache_collection = self._collection_cache_handler(collection.name)

            for old_file_path in file_paths:
                file_path = cache_collection.add_texture(old_file_path)
                atlas_texture = collection.add_texture(str(file_path), file_path.stem)
                atlas_textures.append(atlas_texture)
                self.atlas_manager.add_texture(cache_collection.collection_name, atlas_texture)

            self.on_textures_added.emit(collection, atlas_textures)

    def export_textures_to_current_collection(self):
        if self.current_collection is not None:
            self.export_textures_to_collection(self.current_collection)

    @overload
    def export_textures_to_collection(self, collection: str): ...

    @overload
    def export_textures_to_collection(self, collection: AtlasCollection): ...

    def export_textures_to_collection(self, collection: AtlasCollection | str):
        if isinstance(collection, str):
            collection = self.atlas_manager.load_collection(collection)
        elif not isinstance(collection, AtlasCollection):
            raise TypeError("Bad collection type")

        window = self.app.activeWindow()
        self.export_textures_dialog = QFileDialog(window)

        dir_path = self.export_textures_dialog.getExistingDirectory(
            window,
            "Select the directory to export the textures",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
            )

        if dir_path:
            export_dir = os.path.join(dir_path, collection.name)
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)

            for texture in collection.textures():
                f = Path(texture.img_path)
                column_str = str(texture.column)
                row_str = str(texture.row)
                new_file_name = f"{column_str},{row_str},{f.name}"
                new_file_path = os.path.join(export_dir, new_file_name)
                shutil.copy(texture.img_path, new_file_path)

    def replace_texture_of_current_collection(self, new_texture: AtlasTexture):
        if self.current_collection is not None:
            self.replace_texture_of_collection(self.current_collection, new_texture)

    def replace_texture_of_collection(self, collection: AtlasCollection | str, new_texture: AtlasTexture):
        if isinstance(collection, str):
            collection = self.atlas_manager.load_collection(collection)
        elif not isinstance(collection, AtlasCollection):
            raise TypeError("Bad collection type")

        cache_collection = self._collection_cache_handler(collection.name)

        old_texture = collection.get_texture(new_texture.row, new_texture.column)
        old_texture_path = old_texture.texture_path
        new_texture_path = new_texture.texture_path
        if old_texture_path != new_texture_path:
            old_texture_name = Path(old_texture_path).name
            new_texture.texture_path = cache_collection.replace_texture(old_texture_name, new_texture_path)

        self.atlas_manager.update_texture(collection.name, new_texture)
        collection.replace_texture(new_texture)
