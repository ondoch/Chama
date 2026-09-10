from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QButtonGroup
)
from PyQt5.QtCore import pyqtSignal
from components.radio_btn import RadioBtn

class RadioButtonGroup(QFrame):
    valueChanged = pyqtSignal(str)

    def __init__(self, header_lbl, options=None, default=None):
        super().__init__()
        self.header_lbl = header_lbl
        self.options = options or ["Male", "Female"]
        self.default = default or self.options[0]
        self.radios = {}
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(6)

        radio_layout = QHBoxLayout()
        radio_layout.setContentsMargins(0, 0, 0, 0)
        radio_layout.setSpacing(20)

        label = QLabel(self.header_lbl)
        label.setStyleSheet("font-family: Segoe UI; font-size: 12px;")

        self.button_group = QButtonGroup(self)

        for option in self.options:
            radio_widget = RadioBtn(option)
            self.radios[option] = radio_widget
            self.button_group.addButton(radio_widget.radio_btn)
            radio_widget.radio_btn.toggled.connect(self._on_toggled)
            radio_layout.addWidget(radio_widget)
        radio_layout.addStretch()

        main_layout.addWidget(label)
        main_layout.addLayout(radio_layout)

        self.set_value(self.default)

    def _on_toggled(self, checked):
        if checked:
            self.valueChanged.emit(self.get_value())

    def get_value(self) -> str:
        for option, radio_widget in self.radios.items():
            if radio_widget.is_checked():
                return option
        return ""

    def set_value(self, value: str):
        if value not in self.radios:
            raise ValueError(f"Invalid value: {value!r}. Expected one of {list(self.radios)}.")
        self.radios[value].set_checked(True)