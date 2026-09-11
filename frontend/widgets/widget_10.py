from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from components.officials_input import OfficialsInput
from components.banner_3 import Banner3
from components.style_constants import (
    COLOR_BORDER,
    FONT_FAMILY,
    COLOR_TEXT_PRIMARY
)

class Official(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        container_widget = QWidget()
        container_widget.setFixedWidth(300)
        container_widget.setObjectName("overall_container")
        container_widget_layout = QVBoxLayout(container_widget)

        header_container = QWidget()
        header_container_layout = QHBoxLayout(header_container)

        icon = QLabel()
        icon.setFixedSize(45,45)
        pixmap = QPixmap("resources/leader.svg")
        icon.setPixmap(pixmap.scaled(43,43, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        banner = Banner3()

        header_label = QLabel("Assign chama officials")
        header_label.setObjectName("header_label")

        header_container_layout.addWidget(icon)
        header_container_layout.addWidget(header_label)

        main_layout.setAlignment(Qt.AlignCenter)

        choice_1 = OfficialsInput("Chairperson")
        choice_2 = OfficialsInput("Secretary")
        choice_3 = OfficialsInput("Treasurer")

        container_widget_layout.addWidget(banner)
        container_widget_layout.addWidget(header_container)
        container_widget_layout.addWidget(choice_1)
        container_widget_layout.addWidget(choice_2)
        container_widget_layout.addWidget(choice_3)

        main_layout.addWidget(container_widget)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#overall_container{{
                border: 1px solid {COLOR_BORDER};
                border-radius: 6px
            }}
            QLabel#header_label{{
                font-family: '{FONT_FAMILY}';
                font-size: 16px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
        """)
