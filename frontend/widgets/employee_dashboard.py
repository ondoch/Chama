from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from components.banner_4 import Banner4
from components.form_dropdown import FormDropdown
from components.members_table import MembersTable
from components.pagination import Pagination
from components.search_input import SearchInput
from components.style_constants import (
    COLOR_BORDER,
    COLOR_SIDEBAR_BG,
    COLOR_SIDEBAR_HOVER,
    COLOR_SIDEBAR_SELECT,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    FONT_FAMILY,
)
from modals.employee_information import EmployeeInformation


class EmployeeDashboard(QFrame):

    def __init__(self):
        super().__init__()
        self.employees = []
        self.initUI()
        self.setStylesheet()
        self.updateBanners()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        container_widget = QWidget()
        container_widget.setObjectName("container_widget")
        container_widget_layout = QVBoxLayout(container_widget)

        header_widget = QWidget()
        header_widget_layout = QHBoxLayout(header_widget)
        header_widget_layout.setContentsMargins(20, 0, 0, 0)

        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(10, 0, 0, 0)
        header_widget_layout.setSpacing(0)

        icon = QLabel()
        icon.setFixedSize(50, 50)
        pixmap = QPixmap("resources/employees.svg")
        icon.setPixmap(
            pixmap.scaled(49, 49, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        header = QLabel("Employees")
        header.setObjectName("header")
        label = QLabel("Manage Employees, Roles and Responsibilities")
        label.setObjectName("label")

        header_layout.addWidget(header)
        header_layout.addWidget(label)
        header_widget_layout.addWidget(icon)
        header_widget_layout.addLayout(header_layout)

        self.add_employee_button = QPushButton("+ Add Employee")
        self.add_employee_button.setObjectName("add_chama_button")
        self.add_employee_button.setCursor(Qt.PointingHandCursor)
        self.add_employee_button.setFixedHeight(38)
        self.add_employee_button.clicked.connect(self.openAddEmployee)

        top_row_widget = QWidget()
        top_row_layout = QHBoxLayout(top_row_widget)
        top_row_layout.setContentsMargins(0, 0, 0, 0)

        top_row_layout.addWidget(header_widget, alignment=Qt.AlignLeft)
        top_row_layout.addStretch()
        top_row_layout.addWidget(
            self.add_employee_button,
            alignment=Qt.AlignRight | Qt.AlignVCenter,
        )

        banner_layout = QHBoxLayout()
        banner_layout.setSpacing(12)

        left, top, right, bottom = banner_layout.getContentsMargins()
        banner_layout.setContentsMargins(left, 10, right, bottom)

        self.banner_total = Banner4(
            "resources/employees_1.svg", "0", "Employees"
        )
        self.banner_active = Banner4(
            "resources/active_users.svg", "0", "Active employees"
        )
        self.banner_inactive = Banner4(
            "resources/inactive_users.svg", "0", "Inactive employees"
        )
        self.banner_managed_chamas = Banner4(
            "resources/manage.svg", "0", "Managed chamas"
        )

        banner_layout.addWidget(self.banner_total, stretch=1)
        banner_layout.addWidget(self.banner_active, stretch=1)
        banner_layout.addWidget(self.banner_inactive, stretch=1)
        banner_layout.addWidget(self.banner_managed_chamas, stretch=1)

        search_widget = QWidget()
        search_widget_layout = QHBoxLayout(search_widget)

        # Store references to search input and dropdown
        self.search = SearchInput("Search...")
        self.status_dropdown = FormDropdown(
            "All",
            ["Active", "Inactive", "Onboarding"],
            height=40,
            icon_path="resources/down_arrow.svg",
        )

        # Connect signals to trigger re-filtering
        self.search.textChanged.connect(self.applyFilters)

        # Handle dropdown signal (QComboBox uses currentIndexChanged or currentTextChanged)
        if hasattr(self.status_dropdown, "currentTextChanged"):
            self.status_dropdown.currentTextChanged.connect(self.applyFilters)
        elif hasattr(self.status_dropdown, "combo"):
            self.status_dropdown.combo.currentTextChanged.connect(
                self.applyFilters
            )

        search_widget_layout.addWidget(self.search, alignment=Qt.AlignLeft)
        search_widget_layout.addWidget(
            self.status_dropdown, alignment=Qt.AlignRight
        )

        container_widget_layout.addWidget(top_row_widget)
        container_widget_layout.addLayout(banner_layout)
        container_widget_layout.addWidget(search_widget)

        self.table = MembersTable()
        self.table.populate(self.employees)
        container_widget_layout.addWidget(self.table)

        footer = Pagination()
        container_widget_layout.addWidget(footer, alignment=Qt.AlignBottom)

        main_layout.addWidget(container_widget)

    def applyFilters(self):
        """Combines search query and dropdown selection to filter self.employees."""
        query = self.search.entry.text().strip().lower()

        # Get current selected text from dropdown
        if hasattr(self.status_dropdown, "currentText"):
            selected_status = self.status_dropdown.currentText()
        elif hasattr(self.status_dropdown, "combo"):
            selected_status = self.status_dropdown.combo.currentText()
        else:
            selected_status = "All"

        filtered = []
        for emp in self.employees:
            # Check dropdown status matching
            emp_status = str(emp.get("status", "")).strip()
            status_match = (
                selected_status == "All"
                or emp_status.lower() == selected_status.lower()
            )

            # Check search query across name, email, role, phone, etc.
            text_fields = [
                str(emp.get("name", "")),
                str(emp.get("first_name", "")),
                str(emp.get("last_name", "")),
                str(emp.get("email", "")),
                str(emp.get("role", "")),
                str(emp.get("phone", "")),
            ]
            search_match = (not query) or any(
                query in field.lower() for field in text_fields
            )

            if status_match and search_match:
                filtered.append(emp)

        self.table.populate(filtered)

    def openAddEmployee(self):
        dialog = EmployeeInformation(self)
        if dialog.exec() == QDialog.Accepted:
            self.employees.append(dialog.employee_data)
            self.applyFilters()
            self.updateBanners()

    def removeEmployee(self, index):
        if 0 <= index < len(self.employees):
            del self.employees[index]
            self.applyFilters()
            self.updateBanners()

    def updateBanners(self):
        total_employees = len(self.employees)

        active_employees = sum(
            1
            for e in self.employees
            if str(e.get("status", "Active")).lower() == "active"
        )
        inactive_employees = sum(
            1
            for e in self.employees
            if str(e.get("status", "")).lower() == "inactive"
        )

        total_managed_chamas = 0
        for e in self.employees:
            try:
                total_managed_chamas += int(e.get("chamas_managed", 0))
            except (TypeError, ValueError):
                pass

        self.banner_total.setHeader(total_employees)
        self.banner_active.setHeader(active_employees)
        self.banner_inactive.setHeader(inactive_employees)
        self.banner_managed_chamas.setHeader(total_managed_chamas)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container_widget{{
                border: 1px solid {COLOR_BORDER};
                background-color: #FFFFFF;
                border-radius: 10px;
            }}
            QLabel#header{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 20px;
                font-weight: 600;
            }}
            QLabel#label{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 16px;
            }}
            QPushButton#add_chama_button{{
                font-family: {FONT_FAMILY};
                background-color: {COLOR_SIDEBAR_BG};
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 600;
                border: none;
                border-radius: 6px;
                padding: 0 16px;
            }}
            QPushButton#add_chama_button:hover{{
                background: {COLOR_SIDEBAR_HOVER};
            }}
            QPushButton#add_chama_button:pressed{{
                background: {COLOR_SIDEBAR_SELECT};
            }}
        """)