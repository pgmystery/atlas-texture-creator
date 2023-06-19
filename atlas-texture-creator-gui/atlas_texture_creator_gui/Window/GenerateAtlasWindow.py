from typing import Callable
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QDialog, \
    QSpacerItem, QSizePolicy, QLabel, QSpinBox, QCheckBox

from atlas_texture_creator.atlas_collection import GenerateAtlasOptionsSize, GenerateAtlasOptions
from ..Forms.LabelForm import LabelForm


class GenerateAtlasReturnType(GenerateAtlasOptions):
    file_path: str


class GenerateAtlasWindow(QDialog):
    def __init__(self, generate_atlas_callback: Callable[[GenerateAtlasReturnType], None]):
        super().__init__()
        self.generate_atlas_callback = generate_atlas_callback

        self._layout = QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(10, 0, 10, 0)

        self.atlas_export_path_widget = AtlasExportPath()
        self._layout.addWidget(self.atlas_export_path_widget)

        self.atlas_export_options = AtlasExportOptions()
        self._layout.addWidget(self.atlas_export_options)

        self.buttons = AtlasExportButtons(
            on_cancel_callback=self.close,
            on_generate_atlas_callback=self.generate_atlas,
        )
        self._layout.addWidget(self.buttons)

        width = 250
        height = 180
        self.setFixedSize(width, height)

        self.setLayout(self._layout)

    def generate_atlas(self):
        save_path = self.atlas_export_path_widget.text()
        lock_size = self.atlas_export_options.texture_size()

        result: GenerateAtlasReturnType = GenerateAtlasReturnType(
            file_path=save_path,
            lock_size=lock_size,
        )

        self.generate_atlas_callback(result)
        self.close()

    def show(self):
        save_dir = self.atlas_export_path_widget.show_save_dialog()

        if save_dir == "":
            return

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

        if save_dir != "":
            self.export_path_widget_edit_box.setText(save_dir)

        return save_dir

    def text(self):
        return self.export_path_widget_edit_box.text()


class AtlasExportOption(QWidget):
    def __init__(self, checkbox_label: str, widget: QWidget):
        super().__init__()
        self.checked = False
        self._widget = widget
        self._widget.setDisabled(True)
        _widget = QWidget(self)
        self._layout = layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        _widget.setLayout(layout)

        self.checkbox = QCheckBox(checkbox_label)
        self.checkbox.stateChanged.connect(self.on_check_changed)
        layout.addWidget(self.checkbox)

        self._layout.addWidget(widget)

    def on_check_changed(self):
        self.checked = self.checkbox.isChecked()
        self._widget.setDisabled(not self.checked)


class AtlasExportOptions(AtlasExportOption):
    def __init__(self):
        self._widget = QWidget()
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._width_edit_box = QSpinBox()
        self._width_edit_box.setValue(32)
        self._layout.addWidget(self._width_edit_box)
        self._width_label = QLabel("Width")
        self._layout.addWidget(self._width_label)
        self._height_edit_box = QSpinBox()
        self._height_edit_box.setValue(32)
        self._layout.addWidget(self._height_edit_box)
        self._height_label = QLabel("Height")
        self._layout.addWidget(self._height_label)

        self._widget.setLayout(self._layout)

        super().__init__("Fixed texture size:", self._widget)

    def texture_size(self) -> GenerateAtlasOptionsSize | None:
        if not self.checked:
            return

        width = int(self._width_edit_box.text())
        height = int(self._height_edit_box.text())

        return GenerateAtlasOptionsSize(
            width=width,
            height=height,
        )


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
