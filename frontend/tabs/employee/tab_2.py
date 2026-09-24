from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from widgets.widget_3 import Widget3
from widgets.widget_4 import Widget4
from components.style_constants import COLOR_BORDER, COLOR_ACCENT_BLUE

class Tab2(QFrame):
    previous_clicked = pyqtSignal()
    next_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        container_row = QHBoxLayout()
        container = QWidget()
        container.setObjectName("container_")
        container.setFixedWidth(800)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(5)

        widgets_row = QHBoxLayout()
        widgets_row.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        widgets_row.setSpacing(5)

        self.widget_1 = Widget3()
        self.widget_2 = Widget4()
        widgets_row.addWidget(self.widget_1)
        widgets_row.addWidget(self.widget_2)

        container_layout.addLayout(widgets_row)

        nav_row = QHBoxLayout()
        nav_row.setContentsMargins(0,0,0,0)

        self.previous_btn = QPushButton("Previous")
        self.previous_btn.setIcon(QIcon("resources/left_arrow.svg"))
        self.previous_btn.setIconSize(QSize(16, 16))
        self.previous_btn.setLayoutDirection(Qt.LeftToRight)
        self.previous_btn.setMinimumWidth(100)
        self.previous_btn.setStyleSheet(f"padding: 8px 16px; background-color:{COLOR_ACCENT_BLUE}; color: #FFFFFF; border: none; border-radius: 6px")

        self.next_btn = QPushButton("Next")
        self.next_btn.setIcon(QIcon("resources/right_arrow.svg"))
        self.next_btn.setIconSize(QSize(16, 16))
        self.next_btn.setLayoutDirection(Qt.RightToLeft)
        self.next_btn.setMinimumWidth(100)
        self.next_btn.setStyleSheet(f"padding: 8px 16px; background-color:{COLOR_ACCENT_BLUE}; color: #FFFFFF; border: none; border-radius: 6px")

        for btn in (self.previous_btn, self.next_btn):
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(36)
            btn.setFixedWidth(110)

        self.previous_btn.clicked.connect(self.previous_clicked.emit)
        self.next_btn.clicked.connect(self.next_clicked.emit)

        nav_row.addWidget(self.previous_btn)
        nav_row.addStretch()
        nav_row.addWidget(self.next_btn)

        container_layout.addLayout(nav_row)

        container_row.addStretch()
        container_row.addWidget(container, alignment=Qt.AlignCenter)
        container_row.addStretch()

        main_layout.addLayout(container_row)

        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container_{{
                border: 1px solid {COLOR_BORDER};
                border-radius: 10px;
                background: #FFFFFF;
            }}
            QPushButton {{
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
                background: #FFFFFF;
                color: #111827;
            }}
            QPushButton:hover {{
                background: #F9FAFB;
            }}
            QPushButton:pressed {{
                background: #F0F0F0;
            }}
        """)
