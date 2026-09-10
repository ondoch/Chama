from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout
)
from widgets.widget_6 import RadioButtonGroup

class Radio(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)

        self.gender_widget = RadioButtonGroup("Gender", ["Male", "Female"], default="Male")
        self.marital_widget = RadioButtonGroup("Marital status", ["Single", "Married"], default="Single")

        main_layout.addWidget(self.gender_widget)
        main_layout.addWidget(self.marital_widget)

    def get_gender(self) -> str:
        return self.gender_widget.get_value()

    def set_gender(self, value: str):
        self.gender_widget.set_value(value)

    def get_marital_status(self) -> str:
        return self.marital_widget.get_value()

    def set_marital_status(self, value: str):
        self.marital_widget.set_value(value)