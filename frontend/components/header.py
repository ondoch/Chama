from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QCheckBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from components.style_constants import (
    COLOR_TEXT_PRIMARY, 
    FONT_FAMILY, 
    COLOR_CARD_BG, 
    COLOR_BORDER,
    COLOR_ACCENT_BLUE,
    COLOR_ACCENT_BLUE_BG)

class Header(QFrame):
    def __init__(self, header):
        super().__init__()
        self.header = header
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)

        icon = QLabel()
        icon.setFixedSize(30,30)
        pixmap = QPixmap("resources/group.svg")
        icon.setPixmap(pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        label = QLabel(self.header)
        label.setObjectName("header")

        select_all = QCheckBox("Select all")
        select_all.setObjectName("select_all")

        main_layout.addWidget(icon)
        main_layout.addWidget(label)
        main_layout.addStretch()
        main_layout.addWidget(select_all)

        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QLabel#header {{
                font-family: '{FONT_FAMILY}';
                font-size: 14px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}

            QCheckBox#select_all {{
                font-family: '{FONT_FAMILY}';
                font-size: 13px;
                font-weight: 500;
                color: {COLOR_ACCENT_BLUE};
                background-color: transparent;
                spacing: 8px;
            }}

            QCheckBox#select_all:hover {{
                color: {COLOR_ACCENT_BLUE_BG};
            }}

            QCheckBox#select_all::indicator {{
                width: 15px;
                height: 15px;
            }}

            QCheckBox#select_all::indicator:unchecked {{
                border: 1px solid {COLOR_BORDER};
                border-radius: 4px;
                background-color: {COLOR_CARD_BG};
            }}

            QCheckBox#select_all::indicator:unchecked:hover {{
                border: 1px solid {COLOR_ACCENT_BLUE};
                border-radius: 4px;
                background-color: {COLOR_CARD_BG};
            }}

            QCheckBox#select_all::indicator:checked {{
                border: 1px solid {COLOR_ACCENT_BLUE};
                border-radius: 4px;
                background-color: {COLOR_ACCENT_BLUE};
                image: url('resources/tick.svg');
            }}

            QCheckBox#select_all::indicator:checked:hover {{
                border: 1px solid {COLOR_ACCENT_BLUE};
                border-radius: 4px;
                background-color: {COLOR_ACCENT_BLUE};
            }}
        """)
