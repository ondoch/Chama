from PyQt5.QtWidgets import (
    QVBoxLayout,
    QDialog
)
from widgets.employee_widget import AddEmployee

class EmployeeInformation(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Employee")
        self.setModal(True)

        layout = QVBoxLayout(self)
        self.add_employee = AddEmployee()
        layout.addWidget(self.add_employee)

    def saveValues(self):
        tab_1 = self.add_employee.employee_info.tab_1
        print(tab_1)
