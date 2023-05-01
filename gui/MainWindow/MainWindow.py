from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self, title: str):
        super().__init__()

        self.layout_widget = layout_widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        layout_widget.setLayout(self.layout)

        self.setCentralWidget(layout_widget)
        self.setCentralWidget(layout_widget)

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle(title)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    @property
    def title(self):
        return self.windowTitle()

    @title.setter
    def title(self, title: str):
        self.setWindowTitle(title)

    def add_widget(self, widget: QWidget):
        self.layout.addWidget(widget)
