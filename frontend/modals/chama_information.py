from PyQt5.QtWidgets import QDialog, QVBoxLayout
from widgets.chama_widget import AddChama


class ChamaInformation(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Chama")
        self.setModal(True)

        layout = QVBoxLayout(self)
        self.widget = AddChama()
        layout.addWidget(self.widget)

        self.widget.cancel_clicked.connect(self.reject)
