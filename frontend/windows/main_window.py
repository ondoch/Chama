from PyQt5.QtWidgets import (
    QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal

from components.side_bar import Sidebar
from components.top_bar import TopBar
from windows.dashboard import DashboardWindow
from windows.chamas import ChamasWindow
from windows.employees import EmployeeWindow
from windows.onboarding import OnboardingWindow
from windows.assignments import AssignmentsWindow
from windows.reports import ReportsWindow
from windows.audit_logs import AuditLogWindow


class MainWindow(QWidget):
    logged_out = pyqtSignal()

    def __init__(self, api, user_data=None):
        super().__init__()
        self.api = api
        self.user_data = user_data or {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        container_widget = QWidget()
        container_widget_layout = QVBoxLayout(container_widget)
        container_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.top_bar = TopBar()
        if self.user_data:
            self.top_bar.update_user(self.user_data)

        side_bar = Sidebar()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(DashboardWindow())     # 0 - Dashboard
        self.stacked_widget.addWidget(ChamasWindow(self.api))        # 1 - Chamas
        self.stacked_widget.addWidget(EmployeeWindow(api=self.api))  # 2 - Employees
        self.stacked_widget.addWidget(OnboardingWindow())    # 3 - Onboarding
        self.stacked_widget.addWidget(AssignmentsWindow())   # 4 - Assignments
        self.stacked_widget.addWidget(ReportsWindow())       # 5 - Reports
        self.stacked_widget.addWidget(AuditLogWindow())      # 6 - Audit logs

        container_widget_layout.addWidget(self.top_bar)
        container_widget_layout.addWidget(self.stacked_widget)

        side_bar.menu_index_selected.connect(self.stacked_widget.setCurrentIndex)
        side_bar.logout_clicked.connect(self.handle_logout)

        self.stacked_widget.setCurrentIndex(0)

        layout.addWidget(side_bar)
        layout.addWidget(container_widget)

    def handle_logout(self) -> None:
        if hasattr(self.api, "logout"):
            self.api.logout()
        self.logged_out.emit()
