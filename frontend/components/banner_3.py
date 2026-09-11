from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)
from PyQt5.QtCore import Qt

from components.style_constants import (
    COLOR_ACCENT_RED_BG,
    COLOR_ACCENT_RED_BORDER,
    FONT_FAMILY
)

class Banner3(QWidget):
    def __init__(self):
         super().__init__()
         self.initUI()
         self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        container = QWidget()
        container.setObjectName("container")
        container_layout = QVBoxLayout(container)
        label = QLabel("Each official role can be assigned to a different member.")
        container_layout.addWidget(label, alignment = Qt.AlignCenter)

        main_layout.addWidget(container)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget{{
                border: 1px solid {COLOR_ACCENT_RED_BORDER};
                background-color: {COLOR_ACCENT_RED_BG};
                border-radius: 4px;
            }}
            QLabel{{
                background:transparent;
                border: none;
                color: {COLOR_ACCENT_RED_BORDER};
                font-family: {FONT_FAMILY};
                font-size: 12px;
            }}
        """)
