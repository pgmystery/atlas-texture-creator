import os
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QFileDialog

from MainWindow import MainWindow
from Toolbar import TopToolbar, BottomToolbar
from TexturesView import TexturesView
from src.atlas_texture_creator import AtlasManager, AtlasCollection


def main():
    def on_new_texture_click():
        file_paths = texture_open_dialog.getOpenFileNames(
            window,
            "Select the texture to add",
            blocks_path,
            images_filter,
            images_filter
        )[0]
        for file_path in file_paths:
            print(file_path)
            f = Path(file_path)
            tv.add_texture(file_path, f.stem)

    parent_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")
    resources_path = os.path.join(parent_path, "resources")
    blocks_path = os.path.join(resources_path, "block", "textures")

    atlas_manager = AtlasManager("")
    atlas_collection = AtlasCollection("")

    app = QApplication()
    window = MainWindow("Atlas Manager")

    texture_open_dialog = QFileDialog(window)
    images_filter = "Images (*.png *.jpg)"

    top_toolbar = TopToolbar(atlas_manager)
    window.addToolBar(Qt.TopToolBarArea, top_toolbar)

    tv = TexturesView(atlas_collection)
    # tv.load_textures(blocks_path)
    window.add_widget(tv)

    bottom_toolbar = BottomToolbar(on_new_texture_click)
    # window.addToolBar(Qt.BottomToolBarArea, bottom_toolbar)
    window.addToolBar(Qt.TopToolBarArea, bottom_toolbar)

    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
