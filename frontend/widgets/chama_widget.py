from PyQt5.QtWidgets import (
    QFrame,
    QStackedWidget,
    QVBoxLayout
)
from PyQt5.QtCore import pyqtSignal

from tabs.chama.tab_1 import Tab1

class AddChama(QFrame):
    cancel_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 500)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        self.tab_1 = Tab1()

        self.tab_1.cancel_clicked.connect(self.cancel_clicked.emit)

        main_layout.addWidget(self.tab_1)
