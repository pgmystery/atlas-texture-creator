import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow
from Toolbar import TopToolbar, BottomToolbar
from TexturesView import TexturesView
from src.atlas_texture_creator import AtlasManager, AtlasCollection


def main():
    def on_new_texture_click():
        atlas_collection.add_texture("", "")
        print(atlas_collection.collection)
        print("LOL")

    parent_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")
    resources_path = os.path.join(parent_path, "resources")
    blocks_path = os.path.join(resources_path, "block", "textures")

    atlas_collection = AtlasCollection()

    app = QApplication()
    window = MainWindow("Atlas Manager")

    top_toolbar = TopToolbar()
    window.addToolBar(Qt.TopToolBarArea, top_toolbar)

    tv = TexturesView()
    tv.load_textures(blocks_path)
    window.add_widget(tv)

    bottom_toolbar = BottomToolbar(on_new_texture_click)
    # window.addToolBar(Qt.BottomToolBarArea, bottom_toolbar)
    window.addToolBar(Qt.TopToolBarArea, bottom_toolbar)

    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
