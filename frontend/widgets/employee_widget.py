from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout
)

from tabs.employee.tab_1 import Tab1
from tabs.employee.tab_2 import Tab2
from tabs.employee.tab_3 import Tab3


class AddEmployee(QFrame):

    CONTENT_WIDTH = 1100

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        outer_vertical = QVBoxLayout(self)
        outer_vertical.setContentsMargins(0, 0, 0, 0)

        content = QWidget()
        content.setFixedWidth(self.CONTENT_WIDTH)

        main_layout = QVBoxLayout(content)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)

        self.stack = QStackedWidget()

        self.tab_1 = Tab1()
        self.tab_2 = Tab2()
        self.tab_3 = Tab3()

        self.tab_2.previous_btn.clicked.connect(self.rolesPermissions)
        #self.tab_2.next_btn.clicked.connect(self.chamaAssignments)
        self.tab_3.previous_btn.clicked.connect(self.employeeInformation)

        self.stack.addWidget(self.tab_1)
        self.stack.addWidget(self.tab_2)
        self.stack.addWidget(self.tab_3)

        main_layout.addWidget(self.stack)

        horizontal_row = QHBoxLayout()
        horizontal_row.addStretch()
        horizontal_row.addWidget(content)
        horizontal_row.addStretch()

        outer_vertical.addStretch()
        outer_vertical.addLayout(horizontal_row)
        outer_vertical.addStretch()

    def employeeInformation(self):
        self.stack.setCurrentIndex(1)

    def rolesPermissions(self):
        self.stack.setCurrentIndex(0)

    def chamaAssignments(self):
        self.stack.setCurrentIndex(2)
