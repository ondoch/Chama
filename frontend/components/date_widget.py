from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtCore import (
    Qt, 
    pyqtSignal, 
    QDate
)
from PyQt5.QtGui import QIntValidator

from components.style_constants import (
    COLOR_BORDER, 
    FONT_FAMILY
)

class DateWidget(QFrame):
    def __init__(self, header):
        super().__init__()
        self.header = header
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignLeft)
        label = QLabel(self.header)
        label.setObjectName("header")
        entry_layout = QHBoxLayout()

        self.day_edit = QLineEdit()
        self.day_edit.setPlaceholderText("D")
        self.day_edit.setValidator(QIntValidator(1, 31, self))
        self.day_edit.setMaxLength(2)
        self.day_edit.setFixedWidth(50)
        self.day_edit.setAlignment(Qt.AlignCenter)

        self.month_edit = QLineEdit()
        self.month_edit = QLineEdit()
        self.month_edit.setPlaceholderText("M")
        self.month_edit.setValidator(QIntValidator(1, 12, self))
        self.month_edit.setMaxLength(2)
        self.month_edit.setFixedWidth(50)
        self.month_edit.setAlignment(Qt.AlignCenter)

        self.year_edit = QLineEdit()
        self.year_edit = QLineEdit()
        self.year_edit.setPlaceholderText("YYYY")
        self.year_edit.setValidator(QIntValidator(1900, 2100, self))
        self.year_edit.setMaxLength(4)
        self.year_edit.setFixedWidth(80)
        self.year_edit.setAlignment(Qt.AlignCenter)

        entry_layout.addWidget(self.day_edit)
        entry_layout.addWidget(self.month_edit)
        entry_layout.addWidget(self.year_edit)

        main_layout.addWidget(label)
        main_layout.addLayout(entry_layout)

    def returnValue(self):
        day_text = self.day_edit.text().strip()
        month_text = self.month_edit.text().strip()
        year_text = self.year_edit.text().strip()

        if not (day_text and month_text and year_text):
            return ""

        day = int(day_text)
        month = int(month_text)
        year = int(year_text)

        date = QDate(year, month, day)

        if not date.isValid():
            return ""

        return date.toString("MMMM d, yyyy")

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QFrame{{
                background: transparent;
            }}
            QLineEdit{{
                border: 1px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 8px 4px;
                font-size: 14px;
                background: white;
            }}
            QLineEdit:focus {{
                border: 1px solid #5b6bf0;
            }}
            QLabel#header{{
                margin:0;
                padding:0;
                border: none;
                background: transparent;
                font-size: 12px;
                font-family: Arial, sans-serif;
            }}
        """)
