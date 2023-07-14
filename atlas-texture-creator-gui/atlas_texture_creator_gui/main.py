import os
import sys
import shutil
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox

from atlas_texture_creator_gui.Window.GenerateAtlasWindow import GenerateAtlasWindow, GenerateAtlasReturnType
from atlas_texture_creator_gui.handlers import CollectionCacheHandler
from atlas_texture_creator_gui.handlers.CollectionCacheHandler import CollectionCache
from .Window import MainWindow
from .Toolbar import AtlasManagerToolbar, AtlasCollectionToolbar
from .TexturesView import TexturesView
from atlas_texture_creator import AtlasManager, AtlasCollection, AtlasTexture


class Application(QApplication):
    def __init__(self):
        super().__init__()
        parent_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
        resources_path = os.path.join(parent_path, "resources")
        blocks_path = os.path.join(resources_path, "block", "textures")

        self._collection_cache_handler = CollectionCacheHandler(".data")

        self.atlas_manager = AtlasManager("")
        self.current_atlas_collection: AtlasCollection | None = None

        self.window = window = MainWindow("Atlas Texture Creator")

        self.generate_atlas_window = GenerateAtlasWindow(self.generate_atlas)

        self.atlas_manager_toolbar = atlas_manager_toolbar = AtlasManagerToolbar(
            new_atlas_collection_callback=self.new_atlas_collection,
            delete_atlas_collection_callback=self.delete_atlas_collection,
            on_atlas_collection_changed=self.current_atlas_collection_changed,
        )
        window.addToolBar(Qt.TopToolBarArea, atlas_manager_toolbar)

        self.tv = tv = TexturesView(
            replace_texture_callback=self.replace_texture
        )
        window.add_widget(tv)

        window.addToolBarBreak(Qt.TopToolBarArea)

        self.atlas_collection_toolbar = atlas_collection_toolbar = AtlasCollectionToolbar(
            add_texture_callback=self.add_textures,
            generate_atlas_callback=self.show_generate_atlas_dialog,
            export_textures_callback=self.export_textures,
            open_path=blocks_path,
        )
        window.addToolBar(Qt.TopToolBarArea, atlas_collection_toolbar)

        self.load_atlas_collections()

        window.show()

        sys.exit(self.exec())

    def current_atlas_collection_changed(self, new_collection_name: str):
        if new_collection_name == "":
            self.current_atlas_collection = None
            self.tv.clear()
        else:
            self.current_atlas_collection = self.atlas_manager.load_collection(new_collection_name)
            self.tv.load_textures(self.current_atlas_collection)

    def load_atlas_collections(self):
        collections = self.atlas_manager.list_collections()
        self.atlas_manager_toolbar.load_atlas_collections(collections)
        if len(collections) == 0:
            self.atlas_collection_toolbar.disable()
        else:
            self.atlas_collection_toolbar.enable()

    def new_atlas_collection(self, collection_name: str):
        self.atlas_manager.create_collection(collection_name)
        self.load_atlas_collections()
        self.atlas_manager_toolbar.set_current_atlas_collection(collection_name)

    def delete_atlas_collection(self, collection_name: str):
        confirm_delete_box = QMessageBox
        answer = confirm_delete_box.question(
            self.window,
            "Delete Collection?",
            f"Do you really want to delete the collection '{collection_name}'?"
            f"\nAll attached textures also getting deleted!",
            QMessageBox.Yes | QMessageBox.No
        )
        if answer == QMessageBox.Yes:
            self.atlas_manager.delete_collection(collection_name)
            cache_collection = self._get_current_cache_collection()
            cache_collection.delete()
            self.load_atlas_collections()

    def add_textures(self, texture_paths: list[str]):
        cache_collection = self._get_current_cache_collection()

        for old_file_path in texture_paths:
            file_path = cache_collection.add_texture(old_file_path)
            atlas_texture = self.current_atlas_collection.add_texture(str(file_path), file_path.stem)
            self.atlas_manager.add_texture(cache_collection.collection_name, atlas_texture)
            self.tv.add_texture(atlas_texture)

    def replace_texture(self, new_texture: AtlasTexture):
        cache_collection = self._get_current_cache_collection()

        old_texture = self.current_atlas_collection.get_texture(new_texture.row, new_texture.column)
        old_texture_path = old_texture.texture_path
        new_texture_path = new_texture.texture_path
        if old_texture_path != new_texture_path:
            old_texture_name = Path(old_texture_path).name
            new_texture.texture_path = cache_collection.replace_texture(old_texture_name, new_texture_path)

        self.atlas_manager.update_texture(self.current_atlas_collection.name, new_texture)
        self.current_atlas_collection.replace_texture(new_texture)
        self.tv.load_textures(self.current_atlas_collection)

    def export_textures(self, dir_path: str):
        export_dir = os.path.join(dir_path, self.current_atlas_collection.name)
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        for texture in self.current_atlas_collection.textures():
            f = Path(texture.img_path)
            column_str = str(texture.column)
            row_str = str(texture.row)
            new_file_name = f"{column_str},{row_str},{f.name}"
            new_file_path = os.path.join(export_dir, new_file_name)
            shutil.copy(texture.img_path, new_file_path)

    def show_generate_atlas_dialog(self):
        self.generate_atlas_window.show()

    def generate_atlas(self, options: GenerateAtlasReturnType):
        save_path = options.file_path
        save_path_dir = os.path.dirname(save_path)
        save_path_obj = Path(save_path)
        texture_coords_path = os.path.join(save_path_dir, f"{save_path_obj.stem}.json")

        img, texture_coords = self.current_atlas_collection.generate_atlas(options)

        img.save(save_path)
        with open(texture_coords_path, 'w') as f:
            f.write(texture_coords.json())

    def _get_current_cache_collection(self) -> CollectionCache:
        current_atlas_collection_name = self.current_atlas_collection.name
        cache_collection = self._collection_cache_handler(current_atlas_collection_name)
        return cache_collection


def start():
    Application()


if __name__ == '__main__':
    start()
