from copy import deepcopy
from typing import Callable
from PIL import Image

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QCloseEvent
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QPushButton, \
    QDockWidget, QWidget, QFileDialog

from atlas_texture_creator import AtlasTexture
from .TexturesView import TextureViewImage


class TextureViewImageInfo(QDockWidget):
    def __init__(self, on_close: Callable, on_save: Callable[[AtlasTexture], None]):
        super().__init__()
        self.tvi: TextureViewImage | None = None
        self.tmp_texture: AtlasTexture | None = None
        self._on_close_callback = on_close
        self._on_save_callback = on_save
        self._widget = widget = QWidget()
        self.setMaximumWidth(200)
        self.setWidget(widget)
        self.layout = layout = QVBoxLayout()
        layout.setSpacing(10)
        widget.setLayout(layout)

        self.texture_open_dialog = QFileDialog(self)
        self.texture_open_dialog_images_filter = "Images (*.png *.jpg)"
        self.texture_view = TextureViewImageInfoTexture(self._on_replace_texture_clicked)
        layout.addWidget(self.texture_view)

        self.texture_name_box = texture_name_box = QLineEdit()
        texture_name_box.textChanged.connect(self._on_texture_name_box_change)
        layout.addWidget(texture_name_box)

        self.size_info = QLabel()
        layout.addWidget(self.size_info)

        self.coord_info = QLabel()
        layout.addWidget(self.coord_info)

        vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(vertical_spacer)

        self.save_button = save_button = QPushButton(text="Save")
        save_button.clicked.connect(self._on_save_clicked)
        layout.addWidget(save_button)

        self.setFeatures(QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable)
        self.setVisible(False)

    def load_tvi_info(self, tvi: TextureViewImage):
        self.tvi = tvi
        self.tmp_texture = deepcopy(tvi.texture)
        image_path = tvi.texture.img_path

        self.texture_view.set_image(image_path)
        self.texture_name_box.setText(tvi.text)
        self.set_texture_size_text(image_path)
        self.set_texture_coord_text(tvi.texture)
        self.setVisible(True)

    def set_texture_size_text(self, image_path: str):
        img = Image.open(image_path)
        size_info_text = f"width: {img.width} - height: {img.height}"
        self.size_info.setText(size_info_text)

    def set_texture_coord_text(self, texture: AtlasTexture):
        coord_info_text = f"Row: {str(texture.row)} - Column: {str(texture.column)}"
        self.coord_info.setText(coord_info_text)

    def closeEvent(self, event: QCloseEvent):
        self._close(event)

    def _on_save_clicked(self, _):
        self._on_save_callback(self.tmp_texture)

    def _close(self, _):
        self.tvi = None
        self._on_close_callback()

    def _on_replace_texture_clicked(self, _):
        new_img_path = self.texture_open_dialog.getOpenFileName(
            self,
            "Select the texture to replace",
            str(self.tvi.texture.img_path),
            self.texture_open_dialog_images_filter,
            self.texture_open_dialog_images_filter
        )[0]
        if new_img_path:
            self.tmp_texture.img_path = new_img_path
            self.texture_view.set_image(new_img_path)
            self.set_texture_size_text(new_img_path)

    def _on_texture_name_box_change(self, _):
        new_text = self.texture_name_box.text()
        if new_text == "":
            self.tmp_texture.label = self.tvi.texture.label
        else:
            self.tmp_texture.label = new_text


class TextureViewImageInfoTexture(QWidget):
    def __init__(self, replace_click_callback: Callable):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.pixmap_label = pixmap_label = QLabel(alignment=Qt.AlignCenter)
        self.pixmap_label.resizeEvent = self._pixmal_label_resize_event
        pixmap_label.setScaledContents(True)
        self.pixmap_label_size = pixmap_label.size()
        layout.addWidget(pixmap_label)
        self.texture_replace_button = texture_replace_button = QPushButton(text="Replace Texture")
        texture_replace_button.clicked.connect(replace_click_callback)
        layout.addWidget(texture_replace_button)

        self.setLayout(layout)

    def set_image(self, image_path: str):
        pixmap = QPixmap(image_path)
        self.pixmap_label.setPixmap(pixmap)

    def _pixmal_label_resize_event(self, event):
        size = event.size()
        width = size.width()
        height = size.height()

        if width != height:
            pixmap = self.pixmap_label.pixmap()
            pixmap = pixmap.scaled(width, width, Qt.KeepAspectRatio)
            self.pixmap_label.setPixmap(pixmap)
