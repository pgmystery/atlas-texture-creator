from typing import Callable

from PySide6.QtWidgets import QToolBar, QPushButton, QComboBox, QInputDialog, QSpacerItem, QSizePolicy, QWidget, \
    QHBoxLayout


class TopToolbar(QToolBar):
    def __init__(self):
        super().__init__()
        new_button = QPushButton("New Atlas")
        new_button.setStatusTip("Create a new atlas-collection")
        new_button.clicked.connect(self.on_new_button_click)
        self.addWidget(new_button)
        load_combo_box = QComboBox()
        self.addWidget(load_combo_box)

    def on_new_button_click(self, s):
        new_atlas_collection_name, is_ok = QInputDialog.getText(self, "Create Atlas-Collection", "Enter your new Atlas-Collection name")
        if is_ok:
            print(new_atlas_collection_name)


class BottomToolbar(QToolBar):
    def __init__(self, add_button_click: Callable):
        self.add_button_click = add_button_click
        super().__init__()
        widget = QWidget(self)
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)

        add_button = QPushButton("Add Texture")
        add_button.clicked.connect(self.on_add_button_click)

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        generate_atlas_button = QPushButton("Generate Atlas")
        generate_atlas_button.clicked.connect(self.generate_atlas)

        layout.addWidget(add_button)
        layout.addItem(spacer)
        layout.addWidget(generate_atlas_button)
        self.addWidget(widget)

    def on_add_button_click(self, _):
        print("ADD_BUTTON_CLICKED")
        self.add_button_click()

    def generate_atlas(self, _):
        print("GENERATE_ATLAS")
