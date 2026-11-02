from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout
)
from components.active_loans import ActiveLoansTable

class ActiveLoans(QFrame):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 10, 0, 0)
        self.pending_approval = ActiveLoansTable()
        main_layout.addWidget(self.pending_approval)

