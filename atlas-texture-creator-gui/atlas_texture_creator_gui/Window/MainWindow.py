from typing import Callable

from PySide6.QtCore import Slot
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout
from pydantic import BaseModel

from atlas_texture_creator import AtlasCollection
from atlas_texture_creator_gui.components.Bars.MenuBar import MenuBarAction, MenuBarSeperatorType, MenuBar, \
    MenuBarSubMenu
from atlas_texture_creator_gui.handlers import AtlasManagerHandler


class ArbitraryBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class MenuBarFileMenu(ArbitraryBaseModel):
    load_collection: MenuBarSubMenu
    quit: MenuBarAction


class MenuBarAtlasMenu(ArbitraryBaseModel):
    new_atlas_collection: MenuBarAction
    delete_atlas_collection: MenuBarAction
    _: MenuBarSeperatorType
    generate_atlas: MenuBarAction


class MenuBarTexturesMenu(ArbitraryBaseModel):
    add_texture: MenuBarAction
    _: MenuBarSeperatorType
    export_textures: MenuBarAction


class MenuBarHelpMenu(ArbitraryBaseModel):
    about: MenuBarAction


class MenuBarType(ArbitraryBaseModel):
    file: MenuBarFileMenu
    atlas: MenuBarAtlasMenu
    textures: MenuBarTexturesMenu
    help: MenuBarHelpMenu


class MainWindow(QMainWindow):
    def __init__(self, title: str):
        super().__init__()

        self.main_widget = main_widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        main_widget.setLayout(self.layout)

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle(title)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

        self.setCentralWidget(main_widget)

    @property
    def title(self):
        return self.windowTitle()

    @title.setter
    def title(self, title: str):
        self.setWindowTitle(title)

    def add_widget(self, widget: QWidget):
        self.layout.addWidget(widget)


class MainWindowMenubar:
    def __init__(
        self,
        window: MainWindow,
        atlas_manager_handler: AtlasManagerHandler,
        exit_callback: Callable,
        about_callback: Callable,
    ):
        self.window = window
        self.atlas_manager_handler = atlas_manager_handler

        self.menu_bar = MenuBar[MenuBarType](
            self.window.menuBar(),
            {
                "file": MenuBarSubMenu(
                    label="&File",
                    menu={
                        "load_collection": MenuBarSubMenu(
                            label="&Load Collection",
                            menu={},
                        ),
                        "quit": MenuBarAction(
                            label="&Quit",
                            action=exit_callback,
                            shortcut="Alt+F4",
                        ),
                    }
                ),
                "atlas": MenuBarSubMenu(
                    label="&Atlas",
                    menu={
                        "new_atlas_collection": MenuBarAction(
                            label="&New Atlas-Collection",
                            action=atlas_manager_handler.create_collection,
                            shortcut="Ctrl+N",
                        ),
                        "delete_atlas_collection": MenuBarAction(
                            label="&Delete selected Atlas-Collection",
                            action=atlas_manager_handler.delete_current_collection,
                            shortcut="Del",
                        ),
                        "---": "---",
                        "generate_atlas": MenuBarAction(
                            label="&Generate Atlas",
                            action=atlas_manager_handler.generate_current_collection_to_atlas,
                            shortcut="Ctrl+G",
                        ),
                    }
                ),
                "textures": MenuBarSubMenu(
                    label="&Textures",
                    menu={
                        "add_texture": MenuBarAction(
                            label="&Add Texture",
                            action=atlas_manager_handler.add_texture_to_current_collection,
                            shortcut="Ctrl+Shift+N",
                        ),
                        "---": "---",
                        "export_textures": MenuBarAction(
                            label="&Export Textures",
                            action=atlas_manager_handler.export_textures_of_current_collection,
                            shortcut="Ctrl+T",
                        ),
                    }
                ),
                "help": MenuBarSubMenu(
                    label="&Help",
                    menu={
                        "about": MenuBarAction(
                            label="&About",
                            action=about_callback,
                            shortcut="F1",
                        ),
                    }
                ),
            }
        )
        self.menu_bar.menu.atlas.delete_atlas_collection.setDisabled(True)
        self.menu_bar.menu.atlas.generate_atlas.setDisabled(True)
        self.menu_bar.menu.textures.add_texture.setDisabled(True)
        self.menu_bar.menu.textures.export_textures.setDisabled(True)

        self.atlas_manager_handler.on_load_collections.connect(self.load_collections)
        self.atlas_manager_handler.on_current_collection_changed.connect(self.load_collections)
        self.atlas_manager_handler.on_current_collection_changed.connect(self.current_collection_changed)
        self.atlas_manager_handler.on_collection_created.connect(self.load_collections)
        self.atlas_manager_handler.on_collection_deleted.connect(self.load_collections)
        self.atlas_manager_handler.on_textures_added.connect(self.on_textures_added)

    @Slot(AtlasCollection)
    def current_collection_changed(self, collection: AtlasCollection | None):
        if collection is None:
            self.menu_bar.menu.atlas.delete_atlas_collection.setDisabled(True)
            self.menu_bar.menu.atlas.generate_atlas.setDisabled(True)
            self.menu_bar.menu.textures.add_texture.setDisabled(True)
            self.menu_bar.menu.textures.export_textures.setDisabled(True)
        if collection is not None:
            self.menu_bar.menu.atlas.delete_atlas_collection.setDisabled(False)
            self.menu_bar.menu.textures.add_texture.setDisabled(False)
            if len(collection) == 0:
                self.menu_bar.menu.atlas.generate_atlas.setDisabled(True)
                self.menu_bar.menu.textures.export_textures.setDisabled(True)
            else:
                self.menu_bar.menu.atlas.generate_atlas.setDisabled(False)
                self.menu_bar.menu.textures.export_textures.setDisabled(False)

    @Slot()
    def load_collections(self):
        class LoadCollection:
            def __init__(self, name: str):
                self.name = name

            def __call__(self, *args, **kwargs):
                atlas_manager_handler.current_collection = self.name

        atlas_manager_handler = self.atlas_manager_handler
        collection_menu = {}
        counter = 0
        collections = self.atlas_manager_handler.collections()
        current_collection = self.atlas_manager_handler.current_collection

        for collection_name in collections:
            action = MenuBarAction(
                label=collection_name,
                action=LoadCollection(collection_name),
            )
            if current_collection is not None and collection_name == current_collection.name:
                action.setDisabled(True)
                action.setCheckable(True)
                action.setChecked(True)
            collection_menu[f"c{counter}"] = action
            counter += 1

        self.menu_bar.menu.file.load_collection.set_menu(collection_menu)
        self.menu_bar.update()

    @Slot(AtlasCollection)
    def on_textures_added(self, collection: AtlasCollection):
        if len(collection) > 0:
            self.menu_bar.menu.atlas.generate_atlas.setDisabled(False)
            self.menu_bar.menu.textures.export_textures.setDisabled(False)
