from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout
)
from widgets.employee_widget import AddEmployee
from widgets.employee_dashboard import EmployeeDashboard

class EmployeeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        widget_1 = AddEmployee()
        widget_2 = EmployeeDashboard()

        layout.addWidget(widget_2)
