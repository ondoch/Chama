from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from widgets.widget_5 import Widget5
from components.style_constants import COLOR_BORDER, COLOR_ACCENT_BLUE

class Tab3(QFrame):
    previous_clicked = pyqtSignal()
    finish_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout()
        container_1 = QWidget()
        container_1.setObjectName("container_1")
        container_1.setFixedWidth(700)
        container_1_layout = QVBoxLayout(container_1)
        container_1_layout.setContentsMargins(20, 20, 20, 20)

        navigation_layout = QHBoxLayout()

        self.previous_btn = QPushButton("Previous")
        self.previous_btn.setIcon(QIcon("resources/left_arrow.svg"))
        self.previous_btn.setIconSize(QSize(16, 16))
        self.previous_btn.setLayoutDirection(Qt.LeftToRight)
        self.previous_btn.setMinimumWidth(100)
        self.previous_btn.setStyleSheet(f"padding: 8px 16px; background-color:{COLOR_ACCENT_BLUE}; color: #FFFFFF; border: none; border-radius: 6px")

        self.finish_btn = QPushButton("Finish") 
        self.finish_btn.setIcon(QIcon("resources/tick.svg"))
        self.finish_btn.setIconSize(QSize(16, 16))
        self.finish_btn.setLayoutDirection(Qt.RightToLeft)
        self.finish_btn.setMinimumWidth(100)
        self.finish_btn.setStyleSheet(f"padding: 8px 16px; background-color:{COLOR_ACCENT_BLUE}; color: #FFFFFF; border: none; border-radius: 6px")

        for btn in (self.previous_btn, self.finish_btn):
            btn.setCursor(Qt.PointingHandCursor)

        self.previous_btn.clicked.connect(self.previous_clicked.emit)
        self.finish_btn.clicked.connect(self.finish_clicked.emit)

        self.widget_1 = Widget5()
        container_1_layout.addWidget(self.widget_1)

        navigation_layout.addWidget(self.previous_btn)
        navigation_layout.addStretch()
        navigation_layout.addWidget(self.finish_btn)

        container_1_layout.addLayout(navigation_layout)

        main_layout.addWidget(container_1)

        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
        QWidget#container_1{{
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
                background-color: #FFFFFF;
            }}
        """)
