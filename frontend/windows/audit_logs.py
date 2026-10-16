from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout
)

from widgets.audit_log_dashboard import AuditLogDashboard

class AuditLogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        widget = AuditLogDashboard()

        layout.addWidget(widget)
