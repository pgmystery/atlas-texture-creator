from typing import Callable

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QDialog, \
    QSpacerItem, QSizePolicy

from ..Forms.LabelForm import LabelForm


class GenerateAtlasWindow(QDialog):
    def __init__(self, generate_atlas_callback: Callable[[str], None]):
        super().__init__()
        self.generate_atlas_callback = generate_atlas_callback

        self._layout = QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(10, 10, 10, 0)

        self.atlas_export_path_widget = AtlasExportPath()
        self._layout.addWidget(self.atlas_export_path_widget)

        self.buttons = AtlasExportButtons(
            on_cancel_callback=self.close,
            on_generate_atlas_callback=self.generate_atlas,
        )
        self._layout.addWidget(self.buttons)

        width = 200
        height = 100
        self.setFixedSize(width, height)

        self.setLayout(self._layout)

    def generate_atlas(self):
        save_path = self.atlas_export_path_widget.text()
        self.generate_atlas_callback(save_path)

    def show(self):
        self.atlas_export_path_widget.show_save_dialog()
        self.exec()


class AtlasExportPath(LabelForm):
    def __init__(self):
        super().__init__(label="Set the atlas-image path:")
        self.save_atlas_dialog = QFileDialog(self)
        self.texture_open_dialog_images_filter = "Images (*.png *.jpg)"

        self.export_path_widget = QWidget(self)
        self.export_path_widget_layout = QHBoxLayout(self)
        self.export_path_widget_layout.setSpacing(5)
        self.export_path_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.export_path_widget.setLayout(self.export_path_widget_layout)

        self.export_path_widget_edit_box = QLineEdit()
        self.export_path_widget_layout.addWidget(self.export_path_widget_edit_box)
        self.export_path_widget_explorer_button = QPushButton("...")
        self.export_path_widget_explorer_button.setMaximumWidth(50)
        self.export_path_widget_explorer_button.clicked.connect(self.show_save_dialog)
        self.export_path_widget_layout.addWidget(self.export_path_widget_explorer_button)

        self.form_widget = self.export_path_widget

    def show_save_dialog(self):
        save_dir = self.save_atlas_dialog.getSaveFileName(
            self,
            "Path to save the atlas-image",
            selectedFilter=self.texture_open_dialog_images_filter,
        )[0]
        self.export_path_widget_edit_box.setText(save_dir)

    def text(self):
        return self.export_path_widget_edit_box.text()


class AtlasExportButtons(QWidget):
    def __init__(self, on_cancel_callback: Callable, on_generate_atlas_callback: Callable):
        super().__init__()
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        generate_atlas_button = QPushButton("Generate Atlas")
        generate_atlas_button.clicked.connect(on_generate_atlas_callback)
        layout.addWidget(generate_atlas_button)

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(on_cancel_callback)
        layout.addWidget(cancel_button)

        self.setLayout(layout)
