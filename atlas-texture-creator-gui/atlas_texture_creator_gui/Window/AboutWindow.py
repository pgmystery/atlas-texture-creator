from importlib.metadata import version

from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QWidget, QVBoxLayout, QPushButton


class AboutWindow(QDialog):
    def __init__(self, icon_path: str, parent: QWidget = None):
        super().__init__(parent)

        atlas_texture_creator_gui_version = version("atlas-texture-creator-gui")
        atlas_texture_creator_version = version("atlas-texture-creator")
        github_url = "https://github.com/pgmystery/atlas-texture-creator"

        self.layout = layout = QVBoxLayout()
        self.info_layout = info_layout = QHBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(30)
        self.info_widget = info_widget = QWidget()
        info_widget.setLayout(info_layout)

        self.icon = icon = QPixmap(icon_path)
        self.icon_label = icon_label = QLabel(self)
        icon_label.setPixmap(icon)
        icon_label.setStyleSheet("QLabel {padding-top: 9px;}")

        self.about_text = about_text = QLabel(self)
        about_text.setText(f"""
            <html>
                <body style="margin: 0;">
                    <h1 style="font-size:20pt;">
                        Atlas Texture Creator
                    </h1>
                    <p>
                        <span>Atlas-Texture-Creator-GUI Version: {atlas_texture_creator_gui_version}</span>
                    </p>
                    <p>
                        <span>Atlas-Texture-Creator Version: {atlas_texture_creator_version}</span>
                    </p>
                    <br>
                    <p>
                        <span>GitHub: <a href="{github_url}">{github_url}</a></span>
                    </p>
                </body>
            </html>
        """)
        about_text.setOpenExternalLinks(True)
        about_text.setTextInteractionFlags(
            about_text.textInteractionFlags() | QtCore.Qt.TextSelectableByMouse | QtCore.Qt.LinksAccessibleByKeyboard
        )
        about_text.setAlignment(QtCore.Qt.AlignTop)

        info_layout.addWidget(icon_label, 0, Qt.AlignTop)
        info_layout.addWidget(about_text, 1, Qt.AlignTop)

        self.close_button = close_button = QPushButton("Close")
        close_button.setFixedSize(80, 24)
        close_button.clicked.connect(self.close)

        layout.addWidget(info_widget)
        layout.addWidget(close_button, 0, Qt.AlignRight)

        self.setLayout(layout)
        self.setFixedSize(460, 250)
        self.setWindowTitle("About Atlas-Texture-Creator")

    def show(self):
        self.exec()
