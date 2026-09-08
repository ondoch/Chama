from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from components.style_constants import COLOR_ACCENT_BLUE, COLOR_ACCENT_BLUE_BG

class Information(QFrame):
    def __init__(self, header, description):
        super().__init__()
        self.header = header
        self.description = description
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 5, 0, 0)
        container_widget = QWidget()
        container_widget.setFixedHeight(40)
        container_widget.setObjectName("container_widget")
        container_layout = QHBoxLayout(container_widget)
        container_layout.setAlignment(Qt.AlignLeft)

        icon = QLabel()
        icon.setFixedSize(20, 20)
        pixmap = QPixmap("resources/info.svg")
        icon.setPixmap(pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        label_1 = QLabel(self.header)
        label_1.setObjectName("label_1")
        label_2 = QLabel(self.description)
        label_2.setObjectName("label_2")
        container_layout.addWidget(icon)
        container_layout.addWidget(label_1)
        container_layout.addWidget(label_2) 

        main_layout.addWidget(container_widget)
        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container_widget{{
                background-color: {COLOR_ACCENT_BLUE_BG};
                border: 1px solid {COLOR_ACCENT_BLUE};
                border-radius: 6px;
            }}
            QLabel#label_1{{
                color: {COLOR_ACCENT_BLUE};
                font-weight: bold;
            }}
            QLabel#label_2{{
                color: {COLOR_ACCENT_BLUE};
            }}
        """)
