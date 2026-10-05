from PyQt5.QtWidgets import QWidget, QHBoxLayout

from widgets.chama_dashboard import ChamaDashboard


class ChamasWindow(QWidget):
    def __init__(self, api_client):
        super().__init__()

        self.api = api_client

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        widget = ChamaDashboard(self.api)

        layout.addWidget(widget)
