from pydantic import BaseModel

from atlas_texture_creator_gui.components.Bars.MenuBar import MenuBarAction, MenuBarSeperatorType


class ArbitraryBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class MenuBarFileMenu(ArbitraryBaseModel):
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
