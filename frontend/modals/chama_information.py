from PyQt5.QtWidgets import QDialog, QVBoxLayout
from widgets.chama_widget import AddChama


class ChamaInformation(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Chama")
        self.setModal(True)

        self.values = {}

        layout = QVBoxLayout(self)
        self.chama_info = AddChama()
        layout.addWidget(self.chama_info)
        self.chama_info.cancel_clicked.connect(self.reject)

        self.chama_info.tab_1.next_clicked.connect(self.saveValues)

    def saveValues(self):
        self.values = {
            "chama_name": self.chama_info.tab_1.chama_name.returnValue(),
            "description": self.chama_info.tab_1.description.returnValue(),
            "contribution": self.chama_info.tab_1.contribution.returnValue(),
            "pool_percentage": self.chama_info.tab_1.pool_percentage.returnValue(),
            "registration_number": self.chama_info.tab_1.registration_number.returnValue(),
            "meeting_frequency": self.chama_info.tab_1.meeting_frequency.returnValue(),
            "share_percentage": self.chama_info.tab_1.share_percentage.returnValue(),
            "loan_percentage": self.chama_info.tab_1.loan_percentage.returnValue(),
        }
        self.accept()
