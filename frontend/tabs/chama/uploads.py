from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout
)
from PyQt5.QtCore import (
    Qt, 
    pyqtSignal,
    QSize
)
from PyQt5.QtGui import QIcon

from components.member_form_input import MemberFormInput
from components.date_widget import DateWidget
from components.style_constants import (
    COLOR_CARD_BG, 
    COLOR_BORDER, 
    COLOR_ACCENT_BLUE,
    COLOR_TEXT_MUTED
)
from components.upload_widget import UploadWidget
from components.progress_widget import ProgressWidget
from widgets.widget_7 import Radio
from widgets.widget_8 import UploadContainer

class Uploads(QFrame):
    previous_clicked = pyqtSignal()
    add_member_clicked = pyqtSignal()
    finish_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        container_widget = QWidget()
        container_widget.setFixedWidth(1100)
        container_widget.setObjectName("container")
        container_widget_layout = QVBoxLayout(container_widget)

        upload_container = QHBoxLayout()
        upload_1 = UploadContainer("National I.D")
        upload_2 = UploadContainer("K.R.A Certificate")
        upload_3 = UploadContainer("Passport photo")
        upload_container.addWidget(upload_1)
        upload_container.addWidget(upload_2)
        upload_container.addWidget(upload_3)

        header = QLabel("Uploads")
        header.setStyleSheet(f"font-family: Segoe UI; color:{COLOR_TEXT_MUTED}; font-size:20px; font-weight:600;")
        main_layout.addWidget(header, alignment=Qt.AlignCenter)

        nav_row = QHBoxLayout()
        nav_row.setContentsMargins(10, 0, 10, 0)

        self.previous_btn = QPushButton("Previous")
        self.previous_btn.setIcon(QIcon("resources/left_black.svg"))
        self.previous_btn.setIconSize(QSize(16, 16))
        self.previous_btn.setLayoutDirection(Qt.LeftToRight)
        self.previous_btn.setMinimumWidth(100)
        self.previous_btn.setStyleSheet(f"padding: 8px 16px; border:1px solid {COLOR_ACCENT_BLUE}; color: #000; border-radius: 6px")
        self.previous_btn.setCursor(Qt.PointingHandCursor)

        self.add_btn = QPushButton("Add Member")
        self.add_btn.setIcon(QIcon("resources/add.svg"))
        self.add_btn.setIconSize(QSize(16, 16))
        self.add_btn.setLayoutDirection(Qt.LeftToRight)
        self.add_btn.setMinimumWidth(100)
        self.add_btn.setStyleSheet(f"padding: 8px 16px; border:1px solid {COLOR_ACCENT_BLUE}; color: #000; border-radius: 6px")
        self.add_btn.setCursor(Qt.PointingHandCursor)

        self.finish_btn = QPushButton("Finish")
        self.finish_btn.setIcon(QIcon("resources/tick.svg"))
        self.finish_btn.setIconSize(QSize(16, 16))
        self.finish_btn.setLayoutDirection(Qt.RightToLeft)
        self.finish_btn.setMinimumWidth(100)
        self.finish_btn.setStyleSheet(f"padding: 8px 16px; background-color:{COLOR_ACCENT_BLUE}; color: #FFFFFF; border: none; border-radius: 6px")
        self.finish_btn.setCursor(Qt.PointingHandCursor)

        self.previous_btn.clicked.connect(self.previous_clicked.emit)
        self.finish_btn.clicked.connect(self.finish_clicked.emit)

        nav_row.addWidget(self.previous_btn)
        nav_row.addStretch()
        nav_row.addWidget(self.add_btn)
        nav_row.addStretch()
        nav_row.addWidget(self.finish_btn)

        container_widget_layout.addLayout(upload_container)
        container_widget_layout.addLayout(nav_row)

        main_layout.addWidget(container_widget)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container{{
                background: {COLOR_CARD_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
            }}
        """)
