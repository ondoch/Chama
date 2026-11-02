from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout
)
from components.repaid_loans_table import RepaidLoansTable

class RepaidLoans(QFrame):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 10, 0, 0)
        self.repaid_loans = RepaidLoansTable()
        main_layout.addWidget(self.repaid_loans)

