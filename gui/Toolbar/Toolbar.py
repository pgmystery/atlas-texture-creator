from typing import Callable

from PySide6.QtWidgets import QToolBar, QPushButton, QComboBox, QInputDialog, QSpacerItem, QSizePolicy, QWidget, \
    QHBoxLayout, QFileDialog

from atlas_texture_creator import AtlasCollection


class AtlasManagerToolbar(QToolBar):
    def __init__(
        self,
        new_atlas_collection_callback: Callable[[str], None],
        delete_atlas_collection_callback: Callable[[str], None],
        on_atlas_collection_changed: Callable[[str], None],
    ):
        super().__init__()
        self.new_atlas_collection_callback = new_atlas_collection_callback
        self.delete_atlas_collection_callback = delete_atlas_collection_callback
        self.on_atlas_collection_changed = on_atlas_collection_changed
        new_button = QPushButton("New Atlas")
        new_button.setStatusTip("Create a new atlas-collection")
        new_button.clicked.connect(self.on_new_button_click)
        self.addWidget(new_button)
        self.load_combo_box = load_combo_box = QComboBox()
        self.load_combo_box.setFixedWidth(200)
        self.load_combo_box.currentTextChanged.connect(self.current_atlas_collection_changed)
        self.addWidget(load_combo_box)
        # spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.delete_button = QPushButton("Delete Atlas Collection")
        self.delete_button.clicked.connect(self.delete_atlas_collection)
        self.addWidget(self.delete_button)
        layout = self.layout()
        layout.setSpacing(10)

    def on_new_button_click(self, _):
        new_atlas_collection_name, is_ok = QInputDialog.getText(self, "Create Atlas-Collection", "Enter your new Atlas-Collection name")
        if is_ok:
            self.new_atlas_collection_callback(new_atlas_collection_name)

    def current_atlas_collection_changed(self, new_atlas_collection_name):
        self.on_atlas_collection_changed(new_atlas_collection_name)

    def set_current_atlas_collection(self, collection_name: str):
        index = self.load_combo_box.findText(collection_name)
        self.load_combo_box.setCurrentIndex(index)

    def load_atlas_collections(self, collections: list[AtlasCollection]):
        self.load_combo_box.clear()
        if len(collections) == 0:
            self.load_combo_box.setDisabled(True)
            self.delete_button.setDisabled(True)
        else:
            self.load_combo_box.setDisabled(False)
            self.delete_button.setDisabled(False)
            for collection in collections:
                self.load_combo_box.addItem(collection.name)

    def delete_atlas_collection(self, _):
        collection_name = self.load_combo_box.currentText()
        self.delete_atlas_collection_callback(collection_name)


class AtlasCollectionToolbar(QToolBar):
    def __init__(
        self,
        add_texture_callback: Callable[[list[str]], None],
        generate_atlas_callback: Callable,
        open_path: str,
    ):
        super().__init__()
        self.add_texture_callback = add_texture_callback
        self.generate_atlas_callback = generate_atlas_callback
        self.texture_open_dialog = QFileDialog(self)
        self.texture_open_dialog_images_filter = "Images (*.png *.jpg)"
        self.texture_open_dialog_open_path = open_path
        self.save_atlas_dialog = QFileDialog(self)
        widget = QWidget(self)
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)

        self.add_button = add_button = QPushButton("Add Texture")
        add_button.setDisabled(True)
        add_button.clicked.connect(self.on_add_button_click)

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.generate_atlas_button = generate_atlas_button = QPushButton("Generate Atlas")
        generate_atlas_button.setDisabled(True)
        generate_atlas_button.clicked.connect(self.generate_atlas)

        layout.addWidget(add_button)
        layout.addItem(spacer)
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
        self.add_texture_callback(file_paths)

    def generate_atlas(self, _):
        save_dir = self.save_atlas_dialog.getSaveFileName(
            self,
            "Path to save the atlas-image",
            selectedFilter=self.texture_open_dialog_images_filter,
        )[0]
        if save_dir:
            self.generate_atlas_callback(save_dir)

    def disable(self):
        self.add_button.setDisabled(True)
        self.generate_atlas_button.setDisabled(True)

    def enable(self):
        self.add_button.setDisabled(False)
        self.generate_atlas_button.setDisabled(False)
