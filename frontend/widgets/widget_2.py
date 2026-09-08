from PyQt5.QtWidgets import (
    QFrame, 
    QLabel, 
    QWidget, 
    QHBoxLayout, 
    QVBoxLayout, 
    QGridLayout, 
    QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from components.style_constants import (
    FONT_FAMILY, COLOR_TEXT_MUTED, COLOR_ACCENT_BLUE, COLOR_ACCENT_BLUE_BG,
    COLOR_ACCENT_GREEN, COLOR_ACCENT_GREEN_BG, COLOR_ACCENT_GREEN_BORDER, add_shadow
)


class EmployeeSummary(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()
        add_shadow(self, blur=24, y_offset=6)

    def initUI(self):
        self.setObjectName("summary_card")
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(16)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        header_layout.setAlignment(Qt.AlignVCenter)

        body_layout = QGridLayout()
        body_layout.setHorizontalSpacing(16)
        body_layout.setVerticalSpacing(10)
        body_layout.setColumnStretch(1, 1)

        icon = QLabel()
        icon.setAlignment(Qt.AlignCenter)
        icon.setFixedSize(48, 48)
        icon.setObjectName("icon")
        pixmap = QPixmap("resources/user_1.svg")
        icon.setPixmap(pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        sub_header = QVBoxLayout()
        sub_header.setAlignment(Qt.AlignLeft)
        sub_header.setSpacing(4)

        widget = QWidget()
        widget.setObjectName("container")
        widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        widget_layout = QHBoxLayout(widget)
        widget_layout.setContentsMargins(10, 3, 10, 3)

        name = QLabel("John Doe")
        name.setObjectName("name")
        employee_number = QLabel("EMP-0024")
        employee_number.setObjectName("employee_number")

        widget_layout.addWidget(employee_number)
        sub_header.addWidget(name)
        sub_header.addWidget(widget)

        header_layout.addWidget(icon)
        header_layout.addLayout(sub_header)
        header_layout.addStretch()

        job_title_label = QLabel("Job Title:")
        job_title = QLabel("Software Engineer")
        email_label = QLabel("Email:")
        email = QLabel("ondorajoshua75@gmail.com")

        status_widget = QWidget()
        status_widget.setObjectName("status_container")
        status_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(10, 3, 10, 3)

        status_label = QLabel("Status:")
        status = QLabel("Active")
        status.setObjectName("status_label")
        status_layout.addWidget(status)

        for lbl in (job_title_label, job_title, email_label, email, status_label):
            lbl.setObjectName(lbl.objectName() or "meta_label")

        body_layout.addWidget(job_title_label, 0, 0)
        body_layout.addWidget(job_title, 0, 1)
        body_layout.addWidget(email_label, 1, 0)
        body_layout.addWidget(email, 1, 1)
        body_layout.addWidget(status_label, 2, 0)
        body_layout.addWidget(status_widget, 2, 1, alignment=Qt.AlignLeft)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(body_layout)
        self.setFixedWidth(300)
        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QFrame#summary_card {{
                background-color: white;
                border-radius: 12px;
                border: 1px solid #EEF1F4;
            }}
            QWidget#container {{
                background-color: {COLOR_ACCENT_BLUE_BG};
                border-radius: 6px;
            }}
            QWidget#status_container {{
                background-color: {COLOR_ACCENT_GREEN_BG};
                border-radius: 6px;
                border: 1px solid {COLOR_ACCENT_GREEN_BORDER};
            }}
            QLabel#status_label {{
                background: transparent;
                font-family: "{FONT_FAMILY}";
                font-size: 12px;
                font-weight: 600;
                color: {COLOR_ACCENT_GREEN};
            }}
            QLabel#name {{
                color: #1F2937;
                font-weight: 700;
                font-size: 16px;
                font-family: "{FONT_FAMILY}";
                background-color: transparent;
            }}
            QLabel#employee_number {{
                color: {COLOR_ACCENT_BLUE};
                font-weight: 700;
                font-size: 12px;
                background-color: transparent;
            }}
            QLabel#icon {{
                background-color: {COLOR_ACCENT_BLUE_BG};
                border-radius: 24px;
            }}
            QLabel#meta_label {{
                font-family: "{FONT_FAMILY}";
                font-size: 13px;
                color: {COLOR_TEXT_MUTED};
                background-color: transparent;
            }}
        """)