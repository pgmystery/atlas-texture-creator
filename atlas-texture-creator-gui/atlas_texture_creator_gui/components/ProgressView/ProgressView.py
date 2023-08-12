from PySide6.QtCore import Signal, Qt, Slot
from PySide6.QtGui import QFont, QPalette
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, QProgressBar


class ProgressView(QFrame):
    on_finished = Signal()
    step_signal = Signal()

    def __init__(
            self,
            label: str,
            min: int = 0,
            max: int = 100,
            current_value: int = 0,
            add_background: bool = False,
            parent: QWidget = None,
    ):
        super().__init__(parent=parent)

        self.step_signal.connect(self.step)

        self.layout = layout = QVBoxLayout()

        self.frame_layout = frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(20, 10, 20, 10)

        self.top_spacer = top_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(top_spacer)

        window_color = QPalette().window().color().getRgb()
        window_color_r = window_color[0]
        window_color_g = window_color[1]
        window_color_b = window_color[2]
        window_rgb = f"rgb({window_color_r}, {window_color_g}, {window_color_b})"
        self.frame = frame = QFrame()
        if add_background:
            frame.setStyleSheet(f"background-color: {window_rgb};")
        else:
            frame.setStyleSheet(f"background-color: rgba(0,0,0,0%);")
        frame.setLayout(frame_layout)
        layout.addWidget(frame)

        self.bottom_spacer = bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(bottom_spacer)

        self.label = label_widget = QLabel()
        custom_font = QFont()
        custom_font.setPointSize(18)
        label_widget.setFont(custom_font)
        text_color = QPalette().text().color().getRgb()
        text_color_r = text_color[0]
        text_color_g = text_color[1]
        text_color_b = text_color[2]
        text_rgb = f"rgb({text_color_r}, {text_color_g}, {text_color_b})"
        label_widget.setStyleSheet(f"background-color: rgba(0,0,0,0%); color: {text_rgb};")
        label_widget.setText(label)
        self.progress_bar = progress_bar = QProgressBar()
        progress_bar.setAlignment(Qt.AlignCenter)
        progress_bar.setMinimum(min)
        progress_bar.setMaximum(max)
        progress_bar.setValue(current_value)
        progress_bar.valueChanged.connect(self.on_value_changed)

        frame_layout.addWidget(label_widget, 0, Qt.AlignCenter)
        frame_layout.addWidget(progress_bar)

        self.setStyleSheet("background-color: rgba(255, 255, 255, 20);")
        self.setLayout(layout)

    def set_min(self, value: int):
        self.progress_bar.setMinimum(value)

    def get_min(self) -> int:
        return self.progress_bar.minimum()

    def set_max(self, value: int):
        self.progress_bar.setMaximum(value)

    def get_max(self) -> int:
        return self.progress_bar.maximum()

    def set_value(self, value: int):
        self.progress_bar.setValue(value)

    def get_value(self) -> int:
        return self.progress_bar.value()

    @Slot()
    def step(self) -> int:
        current_value = self.progress_bar.value()
        new_value = current_value + 1

        if new_value > self.progress_bar.maximum():
            return current_value

        self.set_value(new_value)

        return new_value

    @Slot(int)
    def on_value_changed(self, value: int):
        max = self.progress_bar.maximum()

        if value >= max:
            self.on_finished.emit()
