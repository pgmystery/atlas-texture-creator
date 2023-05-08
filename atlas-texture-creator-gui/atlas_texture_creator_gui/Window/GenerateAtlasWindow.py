from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QDialog

from ..Forms.LabelForm import LabelForm


class GenerateAtlasWindow(QDialog):
    def __init__(self):
        super().__init__()
        self._layout = QVBoxLayout()

        self.atlas_export_path_widget = AtlasExportPath()
        self._layout.addWidget(self.atlas_export_path_widget)
        self.setLayout(self._layout)

        self.setFixedSize(self.size())

    def show(self):
        self.exec()


class AtlasExportPath(LabelForm):
    def __init__(self):
        super().__init__(label="Set the atlas-image path:")
        self.save_atlas_dialog = QFileDialog(self)
        self.texture_open_dialog_images_filter = "Images (*.png *.jpg)"

        self.export_path_widget = QWidget(self)
        self.export_path_widget_layout = QHBoxLayout(self)
        self.export_path_widget.setLayout(self.export_path_widget_layout)

        self.export_path_widget_edit_box = QLineEdit()
        self.export_path_widget_layout.addWidget(self.export_path_widget_edit_box)
        self.export_path_widget_explorer_button = QPushButton("...")
        self.export_path_widget_explorer_button.clicked.connect(self.explorer_button_clicked)
        self.export_path_widget_layout.addWidget(self.export_path_widget_explorer_button)

        self.form_widget = self.export_path_widget

        self.explorer_button_clicked()

    def explorer_button_clicked(self):
        save_dir = self.save_atlas_dialog.getSaveFileName(
            self,
            "Path to save the atlas-image",
            selectedFilter=self.texture_open_dialog_images_filter,
        )[0]
        self.export_path_widget_edit_box.setText(save_dir)
