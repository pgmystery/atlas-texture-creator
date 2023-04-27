import math
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QGridLayout, QWidget, QHBoxLayout

from .TextureViewImage import TextureViewImage
from .TextureViewImageInfo import TextureViewImageInfo
from src.atlas_texture_creator.atlas_texture import AtlasTexture
from src.atlas_texture_creator import AtlasCollection


class TexturesView(QWidget):
    def __init__(self, atlas_collection: AtlasCollection):
        self.atlas_collection = atlas_collection
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

    # def load_textures(self, dir: str):
    #     self.textures = []
    #     image_files = []
    #     for _, _, files in os.walk(dir):
    #         for file in files:
    #             if file.endswith(".png"):
    #                 image_files.append(file)
    #
    #     self.textures.append([])
    #     grid_size = math.ceil(math.sqrt(len(image_files)))
    #     column_counter = 0
    #     row_counter = 0
    #
    #     for file in image_files:
    #         if row_counter == grid_size:
    #             column_counter += 1
    #             row_counter = 0
    #             self.textures.append([])
    #
    #         file_path = os.path.join(dir, file)
    #         tvi = TextureViewImage(
    #             label=file[:-len(".png")],
    #             img_path=file_path,
    #             x=row_counter,
    #             y=column_counter,
    #             on_click=self.on_texture_click
    #         )
    #         self.texture_view_layout.addWidget(tvi, column_counter, row_counter)
    #         self.textures[column_counter].append(tvi)
    #
    #         row_counter += 1

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
