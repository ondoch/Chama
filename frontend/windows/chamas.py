from PyQt5.QtWidgets import QWidget, QHBoxLayout

from widgets.chama_dashboard import ChamaDashboard
from modals.chama_information import ChamaInformation


class ChamasWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        widget = ChamaDashboard()

        layout.addWidget(widget)
