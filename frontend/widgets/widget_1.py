from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from components.form_input import FormInput
from components.banner import Banner
from components.toggle_button import ToggleSwitch
from components.information import Information

from components.style_constants import COLOR_ACCENT_BLUE

class EmployeePersonalInfo(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        column_layout = QHBoxLayout()
        column_layout.setSpacing(15)

        column_1 = QVBoxLayout()
        column_2 = QVBoxLayout()

        status_layout = QVBoxLayout()
        toggle_layout = QHBoxLayout()
        toggle_layout.setAlignment(Qt.AlignLeft)

        banner = Banner("resources/profile.svg", "Personal Information", "Enter the employee basic details.")
        main_layout.addWidget(banner, alignment=Qt.AlignLeft)

        first_name = FormInput("resources/user.svg", "First Name")
        email_address = FormInput("resources/email.svg", "Email Address")
        national_id = FormInput("resources/id_card.svg", "National ID/Passport number")
        job_title = FormInput("resources/user.svg", "Job Tittle")

        label_1 = QLabel("Status")
        label_1.setStyleSheet("font-size: 13px; font-weight: 500; font-family: 'Segoe UI';")
        label_2 = QLabel("Active")
        label_2.setStyleSheet("font-size: 11px; font-family: 'Segoe UI';")
        label_3 = QLabel("Inactive employees cannot access the system")
        label_3.setStyleSheet("font-size: 11px; font-family: 'Segoe UI'; color: #6B7280;")

        toggle = ToggleSwitch()
        information = Information("Note:", "Employee roles and permissions will be assigned in the next step.")

        last_name = FormInput("resources/user.svg", "Last Name")
        phone_number = FormInput("resources/phone.svg", "Phone Number")
        employee_id = FormInput("resources/emp.svg", "Employment Number")
        employment_date = FormInput("resources/calender.svg", "Employment Date")

        column_1.addWidget(first_name)
        column_1.addWidget(email_address)
        column_1.addWidget(national_id)
        column_1.addWidget(job_title)

        column_2.addWidget(last_name)
        column_2.addWidget(phone_number)
        column_2.addWidget(employee_id)
        column_2.addWidget(employment_date)

        status_layout.addWidget(label_1)
        toggle_layout.addWidget(toggle)
        toggle_layout.addWidget(label_2)
        status_layout.addLayout(toggle_layout)
        status_layout.addSpacing(5)
        status_layout.addWidget(label_3)

        column_layout.addLayout(column_1)
        column_layout.addLayout(column_2)
        main_layout.addLayout(column_layout)

        self.next_button = QPushButton("Next")
        self.next_button.setIcon(QIcon("resources/right_arrow.svg"))
        self.next_button.setIconSize(QSize(16, 16))
        self.next_button.setLayoutDirection(Qt.RightToLeft)
        self.next_button.setMinimumWidth(100)
        self.next_button.setCursor(Qt.PointingHandCursor)
        self.next_button.setStyleSheet(f"padding: 8px 16px; background-color:{COLOR_ACCENT_BLUE}; color: #FFFFFF; border: none; border-radius: 6px")

        bottom_row = QHBoxLayout()
        bottom_row.addLayout(status_layout)
        bottom_row.addStretch()
        bottom_row.addWidget(self.next_button, alignment=Qt.AlignBottom)

        main_layout.addLayout(bottom_row)

        main_layout.addWidget(information)

        self.setLayout(main_layout)
        self.setFixedWidth(600)
