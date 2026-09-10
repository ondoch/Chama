from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout
)
from widgets.chama_widget import AddChama
class ChamasWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        widget = AddChama()
        layout.addWidget(widget)
