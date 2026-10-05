from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout
)
from widgets.employee_widget import AddEmployee
from widgets.employee_dashboard import EmployeeDashboard

class EmployeeWindow(QWidget):
    def __init__(self, api=None):
        super().__init__()

        self.api = api

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        widget = EmployeeDashboard(api_client=self.api)

        layout.addWidget(widget)
