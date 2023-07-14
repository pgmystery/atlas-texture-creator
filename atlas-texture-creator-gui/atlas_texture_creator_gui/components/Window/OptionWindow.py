from enum import Enum
from typing import Callable
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QDialog, \
    QSpacerItem, QSizePolicy
from atlas_texture_creator_gui.components.Forms.LabelForm import LabelForm


class OptionWindowButtons(Enum):
    ONE_BUTTON = 0
    TWO_BUTTONS = 1


class OptionWindowPath(QDialog):
    def __init__(
        self,
        path_title: str,
        width: int = 250,
        height: int = 180,
    ):
        super().__init__()
        self.setFixedSize(width, height)

        self._close_buttons_attached = False
        self._dialog = QFileDialog(self)
        self._dialog_title = ""
        self._dialog_filter = ""

        self.output_dir = ""

        self._create_widgets(path_title)

    def _create_widgets(self, path_title: str):
        self._layout = layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(10, 0, 10, 0)

        self.path_option = PathBoxWidget(path_title, self.open_output_dialog)
        layout.addWidget(self.path_option)

    def open(self):
        if not self._close_buttons_attached:
            self._close_buttons_attached = True



        self.exec()

    def open_from_output_dialog(self, title: str, filter: str = ""):
        self._dialog_title = title
        self._dialog_filter = filter

        self.open_output_dialog()

        if self.output_dir == "":
            return

        self.open()

    def open_output_dialog(self):
        output_dir = self._dialog.getSaveFileName(
            self,
            self._dialog_title,
            selectedFilter=self._dialog_filter,
        )[0]

        return output_dir

    def add_option_widget(self, widget: QWidget):
        self._layout.addWidget(widget)


class CloseButtons(QWidget):
    def __init__(self, on_cancel_callback: Callable, on_save_button: Callable):
        super().__init__()
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # generate_atlas_button = QPushButton("Generate Atlas")
        # generate_atlas_button.clicked.connect(on_generate_atlas_callback)
        # layout.addWidget(generate_atlas_button)

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(on_cancel_callback)
        layout.addWidget(cancel_button)

        self.setLayout(layout)


class PathBoxWidget(LabelForm):
    def __init__(self, label: str, on_select_path_callback: Callable[[], str], button_label: str = "..."):
        super().__init__(label=label)
        self._on_select_path_callback = on_select_path_callback

        self.path_widget = QWidget(self)
        self.path_widget_layout = QHBoxLayout(self)
        self.path_widget_layout.setSpacing(5)
        self.path_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.path_widget.setLayout(self.path_widget_layout)

        self.path_widget_edit_box = QLineEdit()
        self.path_widget_layout.addWidget(self.path_widget_edit_box)
        self.path_widget_explorer_button = QPushButton(button_label)
        self.path_widget_explorer_button.setMaximumWidth(50)
        self.path_widget_explorer_button.clicked.connect(self.open_select_path_dialog)
        self.path_widget_layout.addWidget(self.path_widget_explorer_button)

        self.form_widget = self.path_widget

    def open_select_path_dialog(self):
        dir = self._on_select_path_callback()

        if dir != "":
            self.path_widget_edit_box.setText(dir)

        return dir

    def text(self):
        return self.path_widget_edit_box.text()

    def setText(self, text: str):
        self.path_widget_edit_box.setText(text)
