from PyQt5.QtWidgets import (
    QFrame, 
    QWidget, 
    QHBoxLayout, 
    QVBoxLayout,
    QLabel)
from widgets.widget_1 import EmployeePersonalInfo
from widgets.widget_2 import EmployeeSummary
from components.description import Description
from components.style_constants import COLOR_BORDER, COLOR_PANEL_BG


class Tab1(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        content_layout = QHBoxLayout()

        widget_info = QWidget()
        widget_info.setFixedWidth(650)
        widget_info.setObjectName("widget_info")
        widget_info_layout = QVBoxLayout(widget_info)
        widget_info_layout.setContentsMargins(20, 20, 20, 20)

        self.employee_info = EmployeePersonalInfo()
        widget_info_layout.addWidget(self.employee_info)
        widget_info_layout.addStretch()
        widget_summary = QWidget()
        widget_summary.setObjectName("widget_summary")
        widget_summary_layout = QVBoxLayout(widget_summary)
        widget_summary_layout.setContentsMargins(0, 0, 0, 0)

        employee_summary = EmployeeSummary()

        widget_description = QWidget()
        widget_description.setObjectName("widget_description")
        widget_description_layout = QVBoxLayout(widget_description)
        widget_description_layout.setContentsMargins(20, 20, 20, 20)
        widget_description_layout.setSpacing(0)

        widget_description_layout.addWidget(employee_summary)

        widget_description_layout.addSpacing(16)

        label = QLabel("What's next")
        label.setStyleSheet("font-size: 13px; font-weight: bold;")
        widget_description_layout.addWidget(label)

        for desc in (
            Description(1, "Assign system role(s)", "Define what the employee can do."),
            Description(2, "Assign chama(s)", "Select which chamas they will manage."),
            Description(3, "Set permissions", "Choose specific access rights."),
            Description(4, "Employee can log in", "Access the system with assigned permissions."),
        ):
            widget_description_layout.addWidget(desc)
        widget_description_layout.addStretch()

        widget_summary_layout.addWidget(widget_description)

        content_layout.addWidget(widget_info)
        content_layout.addWidget(widget_summary)

        target_height = max(widget_info.sizeHint().height(), widget_summary.sizeHint().height())
        widget_info.setFixedHeight(target_height)
        widget_summary.setFixedHeight(target_height)

        outer_layout = QVBoxLayout()
        outer_layout.addStretch()
        row = QHBoxLayout()
        row.addStretch()
        row.addLayout(content_layout)
        row.addStretch()
        outer_layout.addLayout(row)
        outer_layout.addStretch()

        self.setLayout(outer_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: transparent;
            }}
            QWidget#widget_info {{
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
                background-color: #FFFFFF;
            }}
            QWidget#widget_summary {{
                border-radius: 12px;
                background-color: {COLOR_PANEL_BG};
            }}
            QWidget#widget_description {{
                background-color: #FFFFFF;
                border-radius: 12px;
            }}
        """)
