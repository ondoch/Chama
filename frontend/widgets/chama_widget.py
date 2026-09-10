from PyQt5.QtWidgets import (
    QFrame,
    QStackedWidget,
    QVBoxLayout
)

from tabs.chama.tab_1 import Tab1
from tabs.chama.tab_2 import Tab2


class AddChama(QFrame):

    CONTENT_WIDTH = 1100

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        self.stack = QStackedWidget()
        tab_1 = Tab1()
        self.tab_2 = Tab2()

        tab_1.next_btn.clicked.connect(self.membersInformation)
        self.tab_2.back_to_tab1.connect(self.chamaInformation)

        self.stack.addWidget(tab_1)
        self.stack.addWidget(self.tab_2)

        main_layout.addWidget(self.stack)

    def chamaInformation(self):
        self.stack.setCurrentIndex(0)

    def membersInformation(self):
        self.stack.setCurrentIndex(1)

    def officilsInformation(self):
        pass