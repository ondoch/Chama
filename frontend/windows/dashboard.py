from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout
)

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        widget = QLabel("Dashboard")

        layout.addWidget(widget)
