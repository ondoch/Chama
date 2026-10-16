from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
)
from widgets.audit_log_dashboard import AuditLogDashboard


class AuditLogWindow(QWidget):
    def __init__(self, api_client):
        super().__init__()

        self.api_client = api_client
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        widget = AuditLogDashboard(self.api_client)

        layout.addWidget(widget)
