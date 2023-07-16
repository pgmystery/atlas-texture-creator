from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QScrollArea, QGridLayout, QWidget, QHBoxLayout

from atlas_texture_creator import AtlasCollection
from .TextureViewImage import TextureViewImage
from .TextureViewImageInfo import TextureViewImageInfo
from atlas_texture_creator.atlas_texture import AtlasTexture


class TexturesView(QWidget):
    def __init__(self, atlas_collection: AtlasCollection = None):
        super().__init__()
        self.atlas_collection = atlas_collection
        self.selected_texture = None
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

        self.tvii = TextureViewImageInfo(self.close_texture_info, self.on_texture_save)
        layout.addWidget(self.tvii)

        self.load_collection(atlas_collection)

    def load_collection(self, atlas_collection: AtlasCollection = None):
        self.atlas_collection = atlas_collection

        if atlas_collection is not None:
            pass

    @Slot(AtlasCollection)
    def on_collection_created(self, collection: AtlasCollection):
        if self.atlas_collection is None:
            self.load_collection(collection)

    @property
    def atlas_collection(self):
        return self._atlas_collection

    @atlas_collection.setter
    def atlas_collection(self, atlas_collection: AtlasCollection = None):
        self._atlas_collection = atlas_collection

        if atlas_collection is not None:
            pass

    def on_texture_click(self, tvi: TextureViewImage):
        if self.selected_texture != tvi:
            if self.selected_texture:
                self.selected_texture.unselect()
            tvi.select()
            self.selected_texture = tvi
            self.tvii.load_tvi_info(tvi)

    def on_texture_save(self, new_texture: AtlasTexture):
        self._replace_texture_callback(new_texture)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Escape:
            self.close_texture_info()

    def close_texture_info(self):
        self.tvii.hide()
        if self.selected_texture:
            self.selected_texture.unselect()
            self.selected_texture = None

    def add_texture(self, texture: AtlasTexture):
        x = texture.row
        y = texture.column

        tvi = TextureViewImage(
            texture=texture,
            on_click=self.on_texture_click,
        )

        self.texture_view_layout.addWidget(tvi, x, y)

    def load_textures(self, collection: AtlasCollection):
        self.clear()
        for texture in collection.textures():
            print(f"id: {str(texture.id)}", f"column: {str(texture.column)}", f"row: {str(texture.row)}")
            self.add_texture(texture)

    def clear(self):
        self.close_texture_info()
        while self.texture_view_layout.count():
            item = self.texture_view_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.texture_view_layout.clearLayout(item.layout())
