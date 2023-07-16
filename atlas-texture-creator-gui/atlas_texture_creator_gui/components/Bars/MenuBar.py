from typing import Callable, Literal, TypeVar, Generic

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu
from pydantic import BaseModel


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


MenuBarMenuType = dict[str, "MenuBarMenuItemType"]


class MenuBarAction(QAction):
    def __init__(self, label: str, action: Callable):
        self.label = label
        self.action = action

        super().__init__()
        self.setText(label)
        self.triggered.connect(action)

    def __str__(self):
        return self.label

    def __call__(self, *args, **kwargs):
        return self.action(*args, **kwargs)


class MenuBarSubMenu(QMenu):
    def __init__(self, label: str, menu: MenuBarMenuType):
        super().__init__()
        self._label = label
        self._menu = menu

        for item_name, item in menu.items():
            setattr(self, item_name, item)

        self.setTitle(label)

    @property
    def label(self):
        return self._label

    @property
    def menu(self):
        return self._menu


class MenuBarSeperator(BaseModel):
    ...


MenuBarSeperatorType = MenuBarSeperator | Literal["---"]
MenuBarMenuItemType = MenuBarSubMenu | MenuBarAction | MenuBarSeperatorType
MenuBarMenuTypeGeneric = TypeVar("MenuBarMenuTypeGeneric", bound=MenuBarMenuType)


class MenuBar(Generic[MenuBarMenuTypeGeneric]):
    def __init__(self, menu_bar: QMenuBar, menu: MenuBarMenuTypeGeneric):
        self.menu_bar = menu_bar
        self.menu: MenuBarMenuTypeGeneric = DotDict(menu)

        self._create_menu(menu_bar, menu)

    def _create_menu(self, menu: QMenuBar | MenuBarSubMenu, sub_menu: MenuBarMenuTypeGeneric):
        for menu_item in sub_menu.values():
            if isinstance(menu_item, MenuBarSubMenu):
                self._create_menu(menu_item, menu_item.menu)
                menu.addMenu(menu_item)

            elif isinstance(menu_item, MenuBarAction):
                menu.addAction(menu_item)

            elif isinstance(menu_item, MenuBarSeperator) or menu_item == "---":
                menu.addSeparator()