from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt5.QtCore import Qt

from components.check_statement import CheckStatement
from components.information import Information
from components.banner import Banner
from components.banner_2 import Banner2

class Widget3(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        container = QWidget()
        container.setFixedWidth(370)
        container_layout = QVBoxLayout(container)

        banner_1 = Banner("resources/roles.svg", "Roles & Permissions", "Assign roles and set specific permission for this employee.")
        banner_2 = Banner2("Employee Roles","Select the roles this employee will have in the system","resources/info.svg")

        check_1 = CheckStatement("Chama Facilitator", "Helps create and onboard chamas, add members and configure basic settings.")
        check_2 = CheckStatement("Chama Supervisor", "Oversees chama facilitators and monitors onboarding progress.")
        check_3 = CheckStatement("Finance Support", "Provides financial support and training (read-only access).")
        check_4 = CheckStatement("Super Administrator", "Fully system access and management.")

        container_layout.addWidget(banner_1, alignment = Qt.AlignLeft)
        container_layout.addWidget(banner_2)
        container_layout.addWidget(check_1)
        container_layout.addWidget(check_2)
        container_layout.addWidget(check_3)
        container_layout.addWidget(check_4)
        container_layout.addStretch()

        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container{{
                background: #FFF;
            }}
        """)
