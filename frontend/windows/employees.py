from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout
)
from widgets.employee_widget import AddEmployee

class EmployeeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        widget = AddEmployee()
        layout.addWidget(widget)
