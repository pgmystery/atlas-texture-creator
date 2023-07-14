from typing import Callable

from PySide6.QtWidgets import QDialog

from atlas_texture_creator_gui.components.Window.OptionWindow import OptionWindowPath


class ExportTexturesWindow(OptionWindowPath):
    # def __init__(self, export_textures_callback: Callable):
    def __init__(self):
        super().__init__("test")


    def show(self):
        # self.exec()
        self.open()
