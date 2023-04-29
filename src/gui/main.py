import os
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QFileDialog

from MainWindow import MainWindow
from Toolbar import TopToolbar, BottomToolbar
from TexturesView import TexturesView
from src.atlas_texture_creator import AtlasManager, AtlasCollection


class Application(QApplication):
    def __init__(self):
        super().__init__()
        parent_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")
        resources_path = os.path.join(parent_path, "resources")
        blocks_path = os.path.join(resources_path, "block", "textures")

        self.atlas_manager = AtlasManager("")
        self.current_atlas_collection = None

        self.window = window = MainWindow("Atlas Manager")

        self.top_toolbar = top_toolbar = TopToolbar(
            new_atlas_collection_callback=self.new_atlas_collection,
            delete_atlas_collection_callback=self.delete_atlas_collection,
            on_atlas_collection_changed=self.current_atlas_collection_changed,
        )
        window.addToolBar(Qt.TopToolBarArea, top_toolbar)

        self.tv = tv = TexturesView()
        window.add_widget(tv)

        self.bottom_toolbar = bottom_toolbar = BottomToolbar(
            add_texture_callback=self.add_textures,
            generate_atlas_callback=self.generate_atlas,
            open_path=blocks_path,
        )
        # window.addToolBar(Qt.BottomToolBarArea, bottom_toolbar)
        window.addToolBar(Qt.TopToolBarArea, bottom_toolbar)

        self.load_atlas_collections()

        window.show()

        sys.exit(self.exec())

    def current_atlas_collection_changed(self, new_collection_name: str):
        print(new_collection_name)

    def load_atlas_collections(self):
        collections = self.atlas_manager.list_atlas_collections()
        self.top_toolbar.load_atlas_collections(collections)
        if len(collections) == 0:
            self.bottom_toolbar.disable()
        else:
            self.bottom_toolbar.enable()

    def new_atlas_collection(self, collection_name: str):
        self.atlas_manager.new_atlas_collection(collection_name)
        self.load_atlas_collections()

    def delete_atlas_collection(self, collection_name: str):
        self.atlas_manager.delete_atlas_collection(collection_name)
        self.load_atlas_collections()

    def add_textures(self, texture_paths: list[str]):
        for file_path in texture_paths:
            print(file_path)
            f = Path(file_path)
            self.tv.add_texture(file_path, f.stem)

    def generate_atlas(self):
        print("GENERATE_ATLAS")


if __name__ == '__main__':
    Application()
