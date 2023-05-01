from typing import Callable, Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QFrame

from atlas_texture_creator.atlas_texture import AtlasTexture


class TextureViewImage(QFrame):
    def __init__(self, texture: AtlasTexture, on_click: Callable[[Any], None]=None):
        self.texture = texture
        self.on_click_callback = on_click
        super().__init__()
        self.layout = layout = QVBoxLayout(self)

        pixmap = QPixmap(texture.texture_path)
        self.pixmap = pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio)
        self.pixmap_label = pixmap_label = QLabel(self, alignment=Qt.AlignCenter)
        pixmap_label.setPixmap(pixmap)
        layout.addWidget(pixmap_label)

        self.label = QLabel(texture.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.label)

        # self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setFrameStyle(QFrame.Panel | QFrame.Plain)

        self.unselect()

        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.on_click_callback(self)

    def select(self):
        self.setLineWidth(1)

    def unselect(self):
        self.setLineWidth(0)

    @property
    def text(self):
        return self.label.text()
