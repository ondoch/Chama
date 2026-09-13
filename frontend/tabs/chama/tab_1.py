from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtCore import (
    Qt, 
    pyqtSignal,
    QSize
)
from PyQt5.QtGui import QIcon

from components.form_input import FormInput
from components.generate_form_input import GenerateFormInput
from components.banner import Banner
from components.style_constants import (
    COLOR_CARD_BG, 
    COLOR_BORDER, 
    COLOR_ACCENT_BLUE
)

class Tab1(QFrame):
    cancel_clicked = pyqtSignal()
    next_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        container_widget = QWidget()
        container_widget.setFixedWidth(800)
        container_widget.setObjectName("container")
        container_widget_layout = QVBoxLayout(container_widget)

        banner = Banner("resources/group_svg.svg", "Basic Information", "Provide fundamental details about the Chama")
        container_widget_layout.addWidget(banner, alignment=Qt.AlignLeft)

        row_container = QWidget()
        row_container_layout = QHBoxLayout(row_container)
        row_container_layout.setSpacing(15)

        row_1 = QVBoxLayout()
        row_2 = QVBoxLayout()

        self.chama_name = FormInput("resources/user.svg", "Chama Name")
        self.description = FormInput("resources/description.svg", "Description of the chama")
        self.contribution = FormInput("resources/contribution.svg", "Amount of contribution")
        self.pool_percentage = FormInput("resources/percent.svg", "Pool percentage e.g 10%")

        self.registration_number = GenerateFormInput("resources/certificate.svg", "Chama registration number")
        self.meeting_frequency = FormInput("resources/calender.svg", "Meeting frequency")
        self.share_percentage = FormInput("resources/percent.svg", "Chama share percentage distribution e.g 10%")
        self.loan_percentage = FormInput("resources/percent.svg", "Loan percentage e.g 10%")

        row_1.addWidget(self.chama_name)
        row_1.addWidget(self.description)
        row_1.addWidget(self.contribution)
        row_1.addWidget(self.pool_percentage)

        row_2.addWidget(self.registration_number)
        row_2.addWidget(self.meeting_frequency)
        row_2.addWidget(self.share_percentage)
        row_2.addWidget(self.loan_percentage)

        row_container_layout.addLayout(row_1)
        row_container_layout.addLayout(row_2)

        nav_row = QHBoxLayout()
        nav_row.setContentsMargins(10,0,10,0)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setIcon(QIcon("resources/cancel.svg"))
        self.cancel_btn.setIconSize(QSize(16, 16))
        self.cancel_btn.setLayoutDirection(Qt.LeftToRight)
        self.cancel_btn.setMinimumWidth(100)
        self.cancel_btn.setStyleSheet(f"padding: 8px 16px; border:1px solid {COLOR_ACCENT_BLUE}; color: #000; border-radius: 6px")

        self.next_btn = QPushButton("Save")
        self.next_btn.setIcon(QIcon("resources/right_arrow.svg"))
        self.next_btn.setIconSize(QSize(16, 16))
        self.next_btn.setLayoutDirection(Qt.RightToLeft)
        self.next_btn.setMinimumWidth(100)
        self.next_btn.setStyleSheet(f"padding: 8px 16px; background-color:{COLOR_ACCENT_BLUE}; color: #FFFFFF; border: none; border-radius: 6px")

        for btn in (self.cancel_btn, self.next_btn):
            btn.setCursor(Qt.PointingHandCursor)

        self.cancel_btn.clicked.connect(self.cancel_clicked.emit)
        self.next_btn.clicked.connect(self.next_clicked.emit)

        nav_row.addWidget(self.cancel_btn)
        nav_row.addStretch()
        nav_row.addWidget(self.next_btn)

        container_widget_layout.addWidget(row_container)
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
