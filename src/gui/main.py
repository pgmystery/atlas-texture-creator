import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow
from Toolbar import TopToolbar, BottomToolbar
from TexturesView import TexturesView


def main():
    parent_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")
    resources_path = os.path.join(parent_path, "resources")
    blocks_path = os.path.join(resources_path, "block", "textures")

    app = QApplication()
    window = MainWindow("Atlas Manager")

    top_toolbar = TopToolbar()
    window.addToolBar(Qt.TopToolBarArea, top_toolbar)

    tv = TexturesView()
    tv.load_textures(blocks_path)
    window.add_widget(tv)

    bottom_toolbar = BottomToolbar()
    # window.addToolBar(Qt.BottomToolBarArea, bottom_toolbar)
    window.addToolBar(Qt.TopToolBarArea, bottom_toolbar)

    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
