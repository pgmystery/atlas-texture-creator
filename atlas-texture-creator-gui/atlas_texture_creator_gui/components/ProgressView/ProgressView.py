from PySide6.QtCore import Signal, Qt, Slot
from PySide6.QtGui import QFont
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
            parent: QWidget = None
    ):
        super().__init__(parent=parent)

        self.step_signal.connect(self.step)

        self.layout = layout = QVBoxLayout()
        layout.setContentsMargins(20, 0, 20, 0)
        self.top_spacer = top_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.label = label_widget = QLabel()
        custom_font = QFont()
        custom_font.setPointSize(18)
        label_widget.setFont(custom_font)
        label_widget.setStyleSheet("background-color: rgba(0,0,0,0%)")
        label_widget.setText(label)
        self.progress_bar = progress_bar = QProgressBar()
        progress_bar.setAlignment(Qt.AlignCenter)
        progress_bar.setMinimum(min)
        progress_bar.setMaximum(max)
        progress_bar.setValue(current_value)
        progress_bar.valueChanged.connect(self.on_value_changed)
        self.bottom_spacer = bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        layout.addItem(top_spacer)
        layout.addWidget(label_widget, 0, Qt.AlignCenter)
        layout.addWidget(progress_bar)
        layout.addItem(bottom_spacer)

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
