from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout
)
from widgets.reports_dashboard import ReportsDashboard

class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        widget = ReportsDashboard()

        layout.addWidget(widget)
