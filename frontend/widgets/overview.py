from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER,
)


class Overview(QFrame):
    def __init__(self):
        super().__init__()

        self.initUi()
        self.setStylesheet()

    def initUi(self):
        main_layout = QHBoxLayout(self)

        container_widget = QWidget()
        container_widget.setObjectName("container_widget")
        container_widget_layout = QVBoxLayout(container_widget)

        label = QLabel("OverView")
        container_widget_layout.addWidget(label)

        main_layout.addWidget(container_widget)

    def setStylesheet(self):
        self.setStyleSheet(f"""
           
        """)
