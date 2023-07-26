import os
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from atlas_texture_creator_gui.handlers import AtlasManagerHandler
from atlas_texture_creator_gui.Window import MainWindow, AboutWindow
from atlas_texture_creator_gui.Window.MainWindow import MainWindowMenubar
from atlas_texture_creator_gui.Toolbar import AtlasManagerToolbar, AtlasCollectionToolbar
from atlas_texture_creator_gui.TexturesView import TexturesView


class AtlasTextureCreatorGUI(QApplication):
    def __init__(self):
        super().__init__()
        cache_dir = ".data"
        self.resources_path = self._get_resources_path()
        self.atlas_manager_handler = AtlasManagerHandler(self, cache_dir)

        self.window = window = MainWindow("Atlas Texture Creator")
        self._load_bars()
        self._load_texture_view()

        self.atlas_manager_handler.load_collections()

        self.setStyle("fusion")
        window.show()

        sys.exit(self.exec())

    def about(self):
        icon_path = self.resources_path / "atlas_texture_creator_icon.png"
        AboutWindow(
            icon_path=str(icon_path),
            parent=self.activeWindow(),
        ).show()

    def _load_bars(self):
        self.atlas_manager_toolbar = atlas_manager_toolbar = AtlasManagerToolbar(
            atlas_manager_handler=self.atlas_manager_handler
        )
        self.window.addToolBar(Qt.TopToolBarArea, atlas_manager_toolbar)
        self.window.addToolBarBreak(Qt.TopToolBarArea)
        self.atlas_collection_toolbar = atlas_collection_toolbar = AtlasCollectionToolbar(
            atlas_manager_handler=self.atlas_manager_handler
        )
        self.window.addToolBar(Qt.TopToolBarArea, atlas_collection_toolbar)
        self.menubar = MainWindowMenubar(
            window=self.window,
            atlas_manager_handler=self.atlas_manager_handler,
            exit_callback=self.exit,
            about_callback=self.about,
        )

    def _load_texture_view(self):
        self.tv = tv = TexturesView(self.atlas_manager_handler)
        self.window.add_widget(tv)

    def _get_resources_path(self) -> Path:
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            resources_path = sys._MEIPASS
        except AttributeError:
            file_path = os.path.dirname(os.path.abspath(__file__))
            resources_path = os.path.join(file_path, "resources")

        resources_path = Path(resources_path)
        return resources_path


def start():
    AtlasTextureCreatorGUI()


if __name__ == '__main__':
    start()
