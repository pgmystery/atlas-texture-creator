from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QGridLayout, QWidget, QHBoxLayout

from .TextureViewImage import TextureViewImage
from .TextureViewImageInfo import TextureViewImageInfo
from src.atlas_texture_creator import AtlasCollection


class TexturesView(QWidget):
    def __init__(self):
        self.atlas_collection = None
        self.selected_img = None
        super().__init__()
        self.layout = layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.texture_view = texture_view = QScrollArea()
        self.frame = frame = QWidget()
        self.texture_view_layout = texture_view_layout = QGridLayout()
        texture_view_layout.setSpacing(0)
        frame.setLayout(texture_view_layout)

        texture_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        texture_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        texture_view.setWidgetResizable(True)
        texture_view.setWidget(frame)
        layout.addWidget(texture_view)

        self.tvii = TextureViewImageInfo(self.close_texture_info)
        layout.addWidget(self.tvii)

    def set_atlas_collection(self, atlas_collection: AtlasCollection):
        self.atlas_collection = atlas_collection

    def on_texture_click(self, tvi: TextureViewImage):
        if self.selected_img != tvi:
            if self.selected_img:
                self.selected_img.unselect()
            tvi.select()
            self.selected_img = tvi
            self.tvii.load_tvi_info(tvi)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Escape:
            self.close_texture_info()

    def close_texture_info(self):
        self.tvii.hide()
        if self.selected_img:
            self.selected_img.unselect()
            self.selected_img = None

    def add_texture(self, file_path: str, label: str):
        texture = self.atlas_collection.add_texture(file_path, label)
        x = texture.row
        y = texture.column

        tvi = TextureViewImage(
            texture=texture,
            on_click=self.on_texture_click,
        )

        self.texture_view_layout.addWidget(tvi, x, y)
