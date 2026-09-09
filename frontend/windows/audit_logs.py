from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout
)

class AuditLogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        widget = QLabel("Audit Logs")

        layout.addWidget(widget)
