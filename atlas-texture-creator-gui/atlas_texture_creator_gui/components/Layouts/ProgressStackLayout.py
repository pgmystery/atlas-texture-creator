from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QStackedLayout

from atlas_texture_creator_gui.components.ProgressView.ProgressView import ProgressView


class ProgressStackLayout(QStackedLayout):
    def __init__(
        self,
        parent: QWidget = None,
    ):
        super().__init__(parent=parent)
        self.progress_view = None

        self.setStackingMode(QStackedLayout.StackAll)

    def show_progress_view(
        self,
        label: str,
        min: int = 0,
        max: int = 100,
        current_value: int = 0,
        add_background: bool = False,
    ):
        if self.progress_view is not None:
            return self.progress_view

        if current_value >= max:
            return None

        self.progress_view = ProgressView(
            label,
            min=min,
            max=max,
            current_value=current_value,
            add_background=add_background
        )
        self.progress_view.on_finished.connect(self.finish_progress_view)
        self.addWidget(self.progress_view)
        self.setCurrentIndex(self.count() - 1)

        return self.progress_view

    @Slot()
    def finish_progress_view(self):
        if self.progress_view is None:
            return

        self.removeWidget(self.progress_view)
        self.progress_view = None
        self.setCurrentIndex(0)
