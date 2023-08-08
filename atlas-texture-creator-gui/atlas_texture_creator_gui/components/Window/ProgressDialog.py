from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QDialog, QWidget

from atlas_texture_creator_gui.components.ProgressView.ProgressView import ProgressView


class ProgressDialog(QDialog):
    on_open = Signal()
    on_cancel = Signal()
    on_finish = Signal()
    close_signal = Signal()

    def __init__(
        self,
        label: str,
        min: int = 0,
        max: int = 100,
        current_value: int = 0,
        show: bool = False,
        width: int = 450,
        height: int = 100,
        parent: QWidget = None
    ):
        super().__init__(parent=parent)

        self.close_signal.connect(self.close)

        self.progress_view = ProgressView(label, min=min, max=max, current_value=current_value, parent=self)

        self.progress_view.progress_bar.valueChanged.connect(self._update_title)
        self.progress_view.on_finished.connect(self._on_progress_finished)

        self.setFixedSize(width, height)
        self.progress_view.setFixedSize(width, height)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setModal(True)

        if show:
            self.show()

    def show(self):
        self._update_title()
        self.on_open.emit()
        self.exec()

    @Slot()
    def _on_progress_finished(self):
        self.close()

    @Slot()
    def _update_title(self):
        self.setWindowTitle(f"{self.progress_view.label.text()} {self.progress_view.progress_bar.text()}")

    def step(self):
        self.progress_view.step_signal.emit()

    def keyPressEvent(self, event: QKeyEvent):
        ...

    @Slot()
    def close(self) -> bool:
        return super().close()
