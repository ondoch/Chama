from PyQt5.QtWidgets import(
    QWidget,
    QLabel,
    QVBoxLayout
)
from components.form_dropdown import FormDropdown
from components.style_constants import (
    FONT_FAMILY
)

class OfficialsInput(QWidget):
    def __init__(self, header):
        super().__init__()
        self.header = header
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        header = QLabel(self.header)
        header.setObjectName("header")
        choices  = FormDropdown(
            "Select a chama...",
            ["Mwangaza Women Chama", "Tumaini Group", "Upendo Chama"],
            height=40,
            icon_path="resources/down_arrow.svg",
        )

        main_layout.addWidget(header)
        main_layout.addWidget(choices)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QLabel#header{{
                font-family: {FONT_FAMILY};
                font-size: 14px;
            }}
        """)
