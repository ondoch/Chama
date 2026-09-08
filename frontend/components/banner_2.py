from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from components.style_constants import FONT_FAMILY, COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED, COLOR_ACCENT_BLUE, COLOR_ACCENT_BLUE_BG

class Banner2(QFrame):
    def __init__(self, header, description, file_path):
        super().__init__()
        self.header = header
        self.description = description
        self.file_path = file_path
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout()

        layout_1 = QHBoxLayout()
        layout_1.setAlignment(Qt.AlignLeft)

        label_1 = QLabel(self.header)
        label_1.setObjectName("header")
        icon = QLabel()
        icon.setFixedSize(20,20)
        pixmap = QPixmap(self.file_path)
        icon.setPixmap(pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label_2 = QLabel(self.description)
        label_2.setObjectName("description")

        layout_1.addWidget(label_1)
        layout_1.addWidget(icon)
        main_layout.addLayout(layout_1)
        main_layout.addWidget(label_2)

        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QLabel#header{{
                font-family: '{FONT_FAMILY}';
                font-size: 14px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
            QLabel#description{{
                font-family: '{FONT_FAMILY}';
                font-size: 13px;
                font-weight: 400;
                color: {COLOR_TEXT_MUTED};
                background-color: transparent;
            }}
        """)
