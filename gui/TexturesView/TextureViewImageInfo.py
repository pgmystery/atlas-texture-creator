from copy import deepcopy
from typing import Callable

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
        layout.setSpacing(0)
        widget.setLayout(layout)

        self.pixmap_label = pixmap_label = QLabel(self, alignment=Qt.AlignCenter)
        pixmap_label.setFixedHeight(pixmap_label.width())
        pixmap_label.setScaledContents(True)
        self.pixmap_label_size = pixmap_label.size()
        layout.addWidget(pixmap_label)
        self.texture_open_dialog = QFileDialog(self)
        self.texture_open_dialog_images_filter = "Images (*.png *.jpg)"
        self.texture_replace_button = texture_replace_button = QPushButton(text="Replace Texture")
        texture_replace_button.clicked.connect(self._on_replace_texture_clicked)
        layout.addWidget(texture_replace_button)

        self.texture_name_box = texture_name_box = QLineEdit()
        texture_name_box.textChanged.connect(self._on_texture_name_box_change)
        layout.addWidget(texture_name_box)

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

        self._show_image(tvi.texture.img_path)
        self.texture_name_box.setText(tvi.text)
        self.setVisible(True)

    def closeEvent(self, event: QCloseEvent):
        self._close(event)

    def _show_image(self, image_path: str):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(self.pixmap_label_size.width(), self.pixmap_label_size.height(), Qt.KeepAspectRatio)
        self.pixmap_label.setPixmap(pixmap)

    def _on_save_clicked(self, _):
        self._on_save_callback(self.tmp_texture)

    def _close(self, _):
        self.tvi = None
        self._on_close_callback()

    def _on_replace_texture_clicked(self, _):
        new_img_path = self.texture_open_dialog.getOpenFileName(
            self,
            "Select the texture to replace",
            self.tvi.texture.img_path,
            self.texture_open_dialog_images_filter,
            self.texture_open_dialog_images_filter
        )[0]
        if new_img_path:
            self.tmp_texture.img_path = new_img_path
            self._show_image(new_img_path)

    def _on_texture_name_box_change(self, _):
        self.tmp_texture.label = self.texture_name_box.text()
