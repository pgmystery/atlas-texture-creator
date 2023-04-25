from PySide6.QtWidgets import QToolBar, QPushButton, QComboBox, QInputDialog


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
    def __init__(self):
        super().__init__()
        add_button = QPushButton("Add Texture")
        add_button.clicked.connect(self.on_add_button_click)
        self.addWidget(add_button)

    def on_add_button_click(self, s):
        print("ADD_BUTTON_CLICKED")
