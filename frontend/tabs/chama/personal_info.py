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
from widgets.widget_7 import Radio

class PersonalInfo(QFrame):
    previous_clicked = pyqtSignal()
    next_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        container_widget = QWidget()
        container_widget.setFixedWidth(750)
        container_widget.setObjectName("container")
        container_widget_layout = QVBoxLayout(container_widget)

        header = QLabel("Personal details")
        header.setStyleSheet(f"font-family: Segoe UI; color:{COLOR_TEXT_MUTED}; font-size:20px; font-weight:600;")
        main_layout.addWidget(header, alignment=Qt.AlignCenter)

        grid = QGridLayout()
        grid.setHorizontalSpacing(2)
        grid.setVerticalSpacing(2)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        full_name = MemberFormInput("Full name (As per I.D/Passport)")
        date_picker = DateWidget("Date of birth")
        phone_number = MemberFormInput("Phone Number")
        email_address = MemberFormInput("Email Address")
        gender = Radio()

        nationality = MemberFormInput("Nationality")
        national_id = MemberFormInput("National I.D/Passport")
        pin = MemberFormInput("KRA Pin")

        grid.addWidget(full_name, 0, 0)
        grid.addWidget(date_picker, 1, 0)
        grid.addWidget(phone_number, 2, 0)
        grid.addWidget(email_address, 3, 0)
        grid.addWidget(gender, 4, 0)

        grid.addWidget(nationality, 0, 1)
        grid.addWidget(national_id, 1, 1)
        grid.addWidget(pin, 2, 1)

        nav_row = QHBoxLayout()
        nav_row.setContentsMargins(10, 0, 10, 0)

        self.previous_btn = QPushButton("Previous")
        self.previous_btn.setIcon(QIcon("resources/left_black.svg"))
        self.previous_btn.setIconSize(QSize(16, 16))
        self.previous_btn.setLayoutDirection(Qt.LeftToRight)
        self.previous_btn.setMinimumWidth(100)
        self.previous_btn.setStyleSheet(f"padding: 8px 16px; border:1px solid {COLOR_ACCENT_BLUE}; color: #000; border-radius: 6px")

        self.next_btn = QPushButton("Save")
        self.next_btn.setIcon(QIcon("resources/right_arrow.svg"))
        self.next_btn.setIconSize(QSize(16, 16))
        self.next_btn.setLayoutDirection(Qt.RightToLeft)
        self.next_btn.setMinimumWidth(100)
        self.next_btn.setStyleSheet(f"padding: 8px 16px; background-color:{COLOR_ACCENT_BLUE}; color: #FFFFFF; border: none; border-radius: 6px")

        for btn in (self.previous_btn, self.next_btn):
            btn.setCursor(Qt.PointingHandCursor)

        self.previous_btn.clicked.connect(self.previous_clicked.emit)
        self.next_btn.clicked.connect(self.next_clicked.emit)

        nav_row.addWidget(self.previous_btn)
        nav_row.addStretch()
        nav_row.addWidget(self.next_btn)

        container_widget_layout.addLayout(grid)
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