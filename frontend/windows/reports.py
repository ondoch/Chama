from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout
)

class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        widget = QLabel("Reports")

        layout.addWidget(widget)
