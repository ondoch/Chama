from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout
)
from components.all_loans_table import AllLoansTable

class AllLoans(QFrame):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 10, 0, 0)
        self.all_loans = AllLoansTable()
        main_layout.addWidget(self.all_loans)

