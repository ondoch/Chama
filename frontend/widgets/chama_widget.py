from PyQt5.QtWidgets import (
    QFrame,
    QStackedWidget,
    QVBoxLayout
)

from tabs.chama.tab_1 import Tab1
from tabs.chama.tab_2 import Tab2
from tabs.chama.tab_3 import Tab3
from tabs.chama.uploads import Uploads


class AddChama(QFrame):

    CONTENT_WIDTH = 1100

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        self.stack = QStackedWidget()
        self.tab_1 = Tab1()
        self.tab_2 = Tab2()
        self.tab_3 = Tab3()

        self.tab_1.next_btn.clicked.connect(self.membersInformation)
        self.tab_2.back_to_tab1.connect(self.chamaInformation)
        self.tab_2.finished.connect(self.officialsInformation)

        self.stack.addWidget(self.tab_1)
        self.stack.addWidget(self.tab_2)
        self.stack.addWidget(self.tab_3)

        main_layout.addWidget(self.stack)

    def chamaInformation(self):
        self.stack.setCurrentIndex(0)

    def membersInformation(self):
        self.stack.setCurrentIndex(1)

    def officialsInformation(self):
        self.stack.setCurrentIndex(2)
