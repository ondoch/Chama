from PyQt5.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QWidget
)
from PyQt5.QtCore import Qt
from components.style_constants import COLOR_BORDER
from components.header import Header
from components.checkbox import CheckBox
class Container_3(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        container = QWidget()
        container.setFixedWidth(350)
        container.setObjectName("system_container")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(0)

        header = Header("System Access")
        self.view_reports = CheckBox("View Reports")
        self.view_audits = CheckBox("View Audits")
        self.manage_employees = CheckBox("Manage Employees")

        container_layout.addWidget(header)
        container_layout.addWidget(self.view_reports)
        container_layout.addWidget(self.view_audits)
        container_layout.addWidget(self.manage_employees)

        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#system_container{{
                background: #FFFFFF;
                border: 1px solid {COLOR_BORDER};
                border-radius: 5px;
            }}
        """)
