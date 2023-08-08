from PySide6.QtCore import Slot
from PySide6.QtWidgets import QToolBar, QPushButton, QComboBox, QSpacerItem, QSizePolicy, QWidget, QHBoxLayout, \
    QFileDialog

from atlas_texture_creator import AtlasCollection
from atlas_texture_creator_gui.handlers import AtlasManagerHandler


class AtlasManagerToolbar(QToolBar):
    def __init__(self, atlas_manager_handler: AtlasManagerHandler):
        super().__init__("Atlas Toolbar")
        self.atlas_manager_handler = atlas_manager_handler

        create_collection_button = QPushButton("New Atlas-Collection")
        create_collection_button.setStatusTip("Create a new atlas-collection")
        create_collection_button.clicked.connect(self.on_create_collection_button_clicked)
        self.addWidget(create_collection_button)
        self.load_combo_box = load_combo_box = QComboBox()
        load_combo_box.setFixedWidth(200)
        self._load_combo_box_changed_connected = False
        self.addWidget(load_combo_box)
        self.delete_collection_button = QPushButton("Delete Atlas-Collection")
        self.delete_collection_button.clicked.connect(self.delete_atlas_collection)
        self.addWidget(self.delete_collection_button)
        layout = self.layout()
        layout.setSpacing(10)

        atlas_manager_handler.on_current_collection_changed.connect(self.on_collection_changed)
        atlas_manager_handler.on_collection_created.connect(self.on_collection_created)
        atlas_manager_handler.on_load_collections.connect(self.load_atlas_collections)
        atlas_manager_handler.on_collection_deleted.connect(self.on_collection_deleted)

    def on_create_collection_button_clicked(self, _):
        self.atlas_manager_handler.create_collection()

    def current_atlas_collection_changed(self, collection_name: str):
        if collection_name == "":
            return

        if self.atlas_manager_handler.current_collection is not None \
        and self.atlas_manager_handler.current_collection.name == collection_name:
            return

        self.atlas_manager_handler.current_collection = collection_name

    def set_current_atlas_collection(self, collection_name: str):
        index = self.load_combo_box.findText(collection_name)
        self.load_combo_box.setCurrentIndex(index)

    @Slot(list)
    def load_atlas_collections(self, collections: list[str]):
        self.load_combo_box.clear()

        for collection_name in collections:
            self.load_combo_box.addItem(collection_name)
        self.load_combo_box.setCurrentIndex(-1)

        if not self._load_combo_box_changed_connected:
            self._load_combo_box_changed_connected = True
            self.load_combo_box.currentTextChanged.connect(self.current_atlas_collection_changed)

        self.refresh_interface()

    @Slot(AtlasCollection)
    def on_collection_created(self, collection: AtlasCollection):
        self.load_combo_box.addItem(collection.name)
        self.refresh_interface()

    def refresh_interface(self):
        collections = [self.load_combo_box.itemText(i) for i in range(self.load_combo_box.count())]

        if len(collections) == 0:
            self.load_combo_box.setDisabled(True)
            self.delete_collection_button.setDisabled(True)
        else:
            self.load_combo_box.setDisabled(False)
            self.delete_collection_button.setDisabled(False)

    def delete_atlas_collection(self, _):
        collection_name = self.load_combo_box.currentText()
        self.atlas_manager_handler.delete_collection(collection_name)

    @Slot(str)
    def on_collection_deleted(self, collection_name: str):
        item_index = self.load_combo_box.findText(collection_name)

        if item_index >= 0:
            self.load_combo_box.removeItem(item_index)
            self.refresh_interface()

    @Slot(AtlasCollection)
    def on_collection_changed(self, collection: AtlasCollection):
        if collection is not None:
            collection_name = collection.name
            if collection_name != self.load_combo_box.currentText():
                self.set_current_atlas_collection(collection_name)


class AtlasCollectionToolbar(QToolBar):
    def __init__(self, atlas_manager_handler: AtlasManagerHandler):
        super().__init__("Collection Toolbar")
        self.atlas_manager_handler = atlas_manager_handler
        self.save_atlas_dialog = QFileDialog(self)
        widget = QWidget(self)
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)

        self.add_button = add_button = QPushButton("Add Texture")
        add_button.setDisabled(True)
        add_button.clicked.connect(self.on_add_button_click)

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.export_textures_button = export_textures_button = QPushButton("Export Textures")
        export_textures_button.setDisabled(True)
        export_textures_button.clicked.connect(self.export_textures)

        self.generate_atlas_button = generate_atlas_button = QPushButton("Generate Atlas")
        generate_atlas_button.setDisabled(True)
        generate_atlas_button.clicked.connect(self.generate_atlas)

        layout.addWidget(add_button)
        layout.addItem(spacer)
        layout.addWidget(export_textures_button)
        layout.addWidget(generate_atlas_button)
        self.addWidget(widget)

        atlas_manager_handler.on_current_collection_changed.connect(self.on_current_collection_changed)
        atlas_manager_handler.on_textures_added.connect(self.check_collection_length)

    def on_add_button_click(self, _):
        self.atlas_manager_handler.add_texture_to_current_collection()

    def generate_atlas(self, _):
        self.atlas_manager_handler.generate_current_collection_to_atlas()

    def export_textures(self, _):
        self.atlas_manager_handler.export_textures_of_current_collection()

    def disable(self):
        self._set_disable(True)

    def enable(self):
        self._set_disable(False)

    def _set_disable(self, state: bool):
        self.add_button.setDisabled(state)
        self.generate_atlas_button.setDisabled(state)
        self.export_textures_button.setDisabled(state)

    @Slot(AtlasCollection)
    def on_current_collection_changed(self, collection: AtlasCollection | None):
        if collection is None:
            self.disable()
        else:
            self.enable()
            self.check_collection_length(collection)

    @Slot(AtlasCollection)
    def check_collection_length(self, collection: AtlasCollection):
        if collection is None:
            self.generate_atlas_button.setDisabled(True)
            self.export_textures_button.setDisabled(True)
            return

        if len(collection) == 0:
            self.generate_atlas_button.setDisabled(True)
            self.export_textures_button.setDisabled(True)
        else:
            self.generate_atlas_button.setDisabled(False)
            self.export_textures_button.setDisabled(False)
