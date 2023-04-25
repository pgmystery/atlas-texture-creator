from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QCloseEvent
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QPushButton, \
    QDockWidget, QWidget

from .TexturesView import TextureViewImage


class TextureViewImageInfo(QDockWidget):
    def __init__(self, on_close: Callable):
        self.on_close = on_close
        super().__init__()
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
        self.texture_replace_button = texture_replace_button = QPushButton(self, text="Replace Texture")
        layout.addWidget(texture_replace_button)

        self.edit_box = edit_box = QLineEdit()
        layout.addWidget(edit_box)

        vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(vertical_spacer)

        self.save_button = save_button = QPushButton(self, text="Save")
        layout.addWidget(save_button)

        self.setFeatures(QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable)
        self.setVisible(False)

    def load_tvi_info(self, tvi: TextureViewImage):
        pixmap = QPixmap(tvi.img_path)
        pixmap = pixmap.scaled(self.pixmap_label_size.width(), self.pixmap_label_size.height(), Qt.KeepAspectRatio)
        self.pixmap_label.setPixmap(pixmap)
        self.edit_box.setText(tvi.text)
        self.setVisible(True)

    def closeEvent(self, event: QCloseEvent):
        self._close(event)

    def _close(self, _):
        self.on_close()
