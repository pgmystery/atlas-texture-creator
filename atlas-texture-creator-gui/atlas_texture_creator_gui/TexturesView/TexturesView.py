import time

from PySide6 import QtCore
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QScrollArea, QGridLayout, QWidget, QHBoxLayout

from atlas_texture_creator import AtlasCollection
from .TextureViewImage import TextureViewImage
from .TextureViewImageInfo import TextureViewImageInfo
from atlas_texture_creator.atlas_texture import AtlasTexture
from atlas_texture_creator_gui.handlers import AtlasManagerHandler
from atlas_texture_creator_gui.components.Layouts import ProgressStackLayout
from atlas_texture_creator_gui.components.ProgressView.ProgressView import ProgressView


class TexturesView(QWidget):
    def __init__(
        self,
        atlas_manager_handler: AtlasManagerHandler,
        atlas_collection: AtlasCollection = None,
        parent: QWidget = None
    ):
        super().__init__(parent)
        self.atlas_manager_handler = atlas_manager_handler
        self.selected_texture = None
        self.texture_view_widget = QWidget(parent=self)
        self.container_layout = container_layout = ProgressStackLayout()
        container_layout.addWidget(self.texture_view_widget)
        self.layout = layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.texture_view = texture_view = QScrollArea()
        self.frame = frame = QWidget(parent=self)
        self.texture_view_layout = texture_view_layout = QGridLayout()
        texture_view_layout.setSpacing(0)
        frame.setLayout(texture_view_layout)

        texture_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        texture_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        texture_view.setWidgetResizable(True)
        texture_view.setWidget(frame)
        layout.addWidget(texture_view)

        self.tvii = TextureViewImageInfo(self.close_texture_info, self.on_texture_save)
        layout.addWidget(self.tvii)
        self.texture_view_widget.setLayout(layout)
        self.setLayout(container_layout)

        self.atlas_collection = atlas_collection
        atlas_manager_handler.on_current_collection_changed.connect(self.on_atlas_collection_changed)
        atlas_manager_handler.on_textures_added.connect(self.add_textures)

    def load_collection(self, atlas_collection: AtlasCollection = None):
        self.atlas_collection = atlas_collection

    @property
    def atlas_collection(self):
        return self._atlas_collection

    @atlas_collection.setter
    def atlas_collection(self, atlas_collection: AtlasCollection = None):
        self._atlas_collection = atlas_collection

        if atlas_collection is None:
            self.clear()
        else:
            self.load_textures(atlas_collection)

        print("ATLAS_COLLECTION_CHANGED")

    @Slot(AtlasCollection)
    def on_atlas_collection_changed(self, collection: AtlasCollection):
        self.atlas_collection = collection

    def on_texture_click(self, tvi: TextureViewImage):
        if self.selected_texture != tvi:
            if self.selected_texture:
                self.selected_texture.unselect()
            tvi.select()
            self.selected_texture = tvi
            self.tvii.load_tvi_info(tvi)

    def on_texture_save(self, new_texture: AtlasTexture):
        self.atlas_manager_handler.replace_texture_of_collection(self._atlas_collection, new_texture)
        self.load_textures(self._atlas_collection)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Escape:
            self.close_texture_info()

    def close_texture_info(self):
        self.tvii.hide()
        if self.selected_texture:
            self.selected_texture.unselect()
            self.selected_texture = None

    @Slot(AtlasCollection, list)
    def add_textures(self, _, textures: list[AtlasTexture]):
        start_time = time.time()

        progress_view = self.container_layout.show_progress_view(
            label="Loading Textures...",
            max=len(textures),
            add_background=True,
        )

        for texture in textures:
            self.add_texture(texture, progress_view, len(textures))

        end_time = time.time()
        print(f"{end_time - start_time} seconds for adding the textures")

    def add_texture(self, texture: AtlasTexture, progress_view: ProgressView, texture_length: int = 0):
        def _add_texture(tvi, x, y):
            self.texture_view_layout.addWidget(tvi, x, y)
            progress_view.step()

        x = texture.row
        y = texture.column

        tvi = TextureViewImage(
            texture=texture,
            on_click=self.on_texture_click,
        )

        if not self.parent().parent().isVisible() or texture_length < 30:
            _add_texture(tvi, x, y)
        else:
            QtCore.QTimer.singleShot(1000, lambda tvi=tvi, x=x, y=y: _add_texture(tvi, x, y))

    def load_textures(self, collection: AtlasCollection):
        self.clear()

        start_time = time.time()

        textures_length = len(collection)
        if textures_length == 0:
            return

        progress_view = self.container_layout.show_progress_view(
            label="Loading Textures...",
            max=textures_length,
            add_background=True,
        )

        for texture in collection:
            self.add_texture(texture, progress_view, len(collection.textures))

        end_time = time.time()
        print(f"{end_time - start_time} seconds for loading the textures")

    def clear(self):
        self.close_texture_info()
        while self.texture_view_layout.count():
            item = self.texture_view_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.texture_view_layout.clearLayout(item.layout())
