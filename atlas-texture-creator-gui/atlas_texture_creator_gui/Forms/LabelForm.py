from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class LabelForm(QWidget):
    def __init__(self, label="", widget: QWidget | None = None):
        super().__init__()
        self._form_widget = None
        self.form_layout = QVBoxLayout()
        self._form_label_widget = QLabel(label)
        self.form_layout.addWidget(self._form_label_widget)
        self._form_widget = widget
        self.setLayout(self.form_layout)

    @property
    def form_label(self):
        return self._form_label_widget.text()

    @form_label.setter
    def form_label(self, text: str):
        self._form_label_widget.setText(text)

    @property
    def form_widget(self):
        return self._form_widget

    @form_widget.setter
    def form_widget(self, widget: QWidget):
        if self._form_widget:
            self.form_layout.removeWidget(self._form_widget)

        self._form_widget = widget
        self.form_layout.addWidget(widget)
