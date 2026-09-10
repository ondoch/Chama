from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QRadioButton,
    QVBoxLayout
)
from PyQt5.QtCore import Qt


class RadioBtn(QFrame):
    def __init__(self, header):
        super().__init__()
        self.header = header
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(4)

        container_widget = QWidget()
        container_widget_layout = QVBoxLayout(container_widget)
        container_widget_layout.setContentsMargins(0, 0, 0, 0)
        container_widget_layout.setSpacing(4)

        label = QLabel(self.header)
        label.setStyleSheet("font-family: Segoe UI; font-size: 12px;")
        self.radio_btn = QRadioButton()

        container_widget_layout.addWidget(label, alignment=Qt.AlignLeft)
        container_widget_layout.addWidget(self.radio_btn, alignment=Qt.AlignLeft)

        main_layout.addWidget(container_widget)

    @property
    def value(self):
        return self.header

    def is_checked(self) -> bool:
        return self.radio_btn.isChecked()

    def set_checked(self, checked: bool = True):
        self.radio_btn.setChecked(checked)