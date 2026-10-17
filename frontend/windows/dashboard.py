from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout
)

from widgets.overall_dashboard import Dashboard

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        widget = Dashboard()

        layout.addWidget(widget)
