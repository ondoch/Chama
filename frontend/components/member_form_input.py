from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QVBoxLayout
)
from components.style_constants import COLOR_BORDER

class MemberFormInput(QFrame):
    def __init__(self, header):
        super().__init__()
        self.header = header
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        header = QLabel(self.header)
        entry = QLineEdit()
        entry.setFixedHeight(40)
        main_layout.addWidget(header)
        main_layout.addWidget(entry)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QFrame{{
                background: transparent;
            }}
            QLabel{{
                border: none;
                background: transparent;
                font-size: 12px;
                font-family: Arial, sans-serif;
            }}
            QLineEdit{{
                border: 1px solid {COLOR_BORDER};
                background: transparent;
                font-size: 12px;
                font-family: Arial, sans-serif;
                border-radius: 5px;
                padding-left: 5px;
            }}
        """)
