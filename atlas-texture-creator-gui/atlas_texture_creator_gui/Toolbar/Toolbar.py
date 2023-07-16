from PySide6.QtCore import Slot
from PySide6.QtWidgets import QToolBar, QPushButton, QComboBox, QSpacerItem, QSizePolicy, QWidget, QHBoxLayout, \
    QFileDialog

from atlas_texture_creator import AtlasCollection
from atlas_texture_creator_gui.handlers import AtlasManagerHandler


class AtlasManagerToolbar(QToolBar):
    def __init__(self, atlas_manager_handler: AtlasManagerHandler):
        super().__init__()
        self.atlas_manager_handler = atlas_manager_handler

        create_collection_button = QPushButton("New Atlas-Collection")
        create_collection_button.setStatusTip("Create a new atlas-collection")
        create_collection_button.clicked.connect(self.on_create_collection_button_clicked)
        self.addWidget(create_collection_button)
        self.load_combo_box = load_combo_box = QComboBox()
        self.load_combo_box.setFixedWidth(200)
        self.load_combo_box.currentTextChanged.connect(self.current_atlas_collection_changed)
        self.addWidget(load_combo_box)
        self.delete_collection_button = QPushButton("Delete Atlas-Collection")
        self.delete_collection_button.clicked.connect(self.delete_atlas_collection)
        self.addWidget(self.delete_collection_button)
        layout = self.layout()
        layout.setSpacing(10)

        atlas_manager_handler.on_collection_created.connect(self.on_collection_created)
        atlas_manager_handler.on_load_collections.connect(self.load_atlas_collections)

    def on_create_collection_button_clicked(self, _):
        self.atlas_manager_handler.create_collection()

    def current_atlas_collection_changed(self, collection_name: str):
        self.atlas_manager_handler.current_collection = collection_name

    def set_current_atlas_collection(self, collection_name: str):
        index = self.load_combo_box.findText(collection_name)
        self.load_combo_box.setCurrentIndex(index)

    @Slot(list)
    def load_atlas_collections(self, collections: list[AtlasCollection]):
        self.load_combo_box.clear()

        for collection in collections:
            self.load_combo_box.addItem(collection.name)

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


class AtlasCollectionToolbar(QToolBar):
    def __init__(self, atlas_manager_handler: AtlasManagerHandler):
        super().__init__()
        self.atlas_manager_handler = atlas_manager_handler
        self.texture_open_dialog = QFileDialog(self)
        self.texture_open_dialog_images_filter = "Images (*.png *.jpg)"
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
        self.export_textures_dialog = QFileDialog(self)

        self.generate_atlas_button = generate_atlas_button = QPushButton("Generate Atlas")
        generate_atlas_button.setDisabled(True)
        generate_atlas_button.clicked.connect(self.generate_atlas)

        layout.addWidget(add_button)
        layout.addItem(spacer)
        layout.addWidget(export_textures_button)
        layout.addWidget(generate_atlas_button)
        self.addWidget(widget)

    def on_add_button_click(self, _):
        file_paths = self.texture_open_dialog.getOpenFileNames(
            self,
            "Select the texture to add",
            self.texture_open_dialog_open_path,
            self.texture_open_dialog_images_filter,
            self.texture_open_dialog_images_filter
        )[0]
        if len(file_paths) > 0:
            self.add_texture_callback(file_paths)

    def generate_atlas(self, _):
        self.generate_atlas_callback()

    def export_textures(self, _):
        dir_path = self.export_textures_dialog.getExistingDirectory(
            self,
            "Select the directory to export the textures",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )
        if dir_path:
            self.export_textures_callback(dir_path)

    def disable(self):
        self._set_disable(True)

    def enable(self):
        self._set_disable(False)

    def _set_disable(self, state: bool):
        self.add_button.setDisabled(state)
        self.generate_atlas_button.setDisabled(state)
        self.export_textures_button.setDisabled(state)
