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

        widget.add_chama_button.clicked.connect(self.addChama)

        layout.addWidget(widget)

    def addChama(self):
        dialog = ChamaInformation(self)
        if dialog.exec_() == ChamaInformation.Accepted:
            values = dialog.values
            print(values)
