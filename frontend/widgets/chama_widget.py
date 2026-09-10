from PyQt5.QtWidgets import (
    QFrame,
    QVBoxLayout
)

from tabs.chama.tab_1 import Tab1


class AddChama(QFrame):

    CONTENT_WIDTH = 1100

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        tab_1 = Tab1()

        main_layout.addWidget(tab_1)
