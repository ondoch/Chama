from PyQt5.QtWidgets import (
    QFrame,
    QStackedWidget,
    QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal

from tabs.chama.personal_info import PersonalInfo
from tabs.chama.residential_info import ResidentialInfo
from tabs.chama.employment_info import EmploymentInfo
from tabs.chama.next_of_kin import NextOfKin
from tabs.chama.uploads import Uploads

class Tab2(QFrame):
    back_to_tab1 = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)
        self.stack = QStackedWidget()

        self.widget_1 = PersonalInfo()
        self.widget_2 = ResidentialInfo()
        self.widget_3 = EmploymentInfo()
        self.widget_4 = NextOfKin()
        self.widget_5 = Uploads()

        self.widget_1.next_btn.clicked.connect(self.residentialInfo)
        self.widget_2.next_btn.clicked.connect(self.employmentInfo)
        self.widget_3.next_btn.clicked.connect(self.nextOfKin)
        self.widget_4.next_btn.clicked.connect(self.uploads)

        self.widget_5.previous_btn.clicked.connect(self.nextOfKin)
        self.widget_4.previous_btn.clicked.connect(self.employmentInfo)
        self.widget_3.previous_btn.clicked.connect(self.residentialInfo)
        self.widget_2.previous_btn.clicked.connect(self.personalInfo)
        self.widget_1.previous_btn.clicked.connect(self.back_to_tab1.emit)

        self.widget_5.add_btn.clicked.connect(self.personalInfo)
        self.widget_5.finish_btn.clicked.connect(self.finished.emit)

        self.stack.addWidget(self.widget_1)
        self.stack.addWidget(self.widget_2)
        self.stack.addWidget(self.widget_3)
        self.stack.addWidget(self.widget_4)
        self.stack.addWidget(self.widget_5)

        main_layout.addWidget(self.stack)

    def personalInfo(self):
        self.stack.setCurrentIndex(0)

    def residentialInfo(self):
        self.stack.setCurrentIndex(1)

    def employmentInfo(self):
        self.stack.setCurrentIndex(2)

    def nextOfKin(self):
        self.stack.setCurrentIndex(3)

    def uploads(self):
        self.stack.setCurrentIndex(4)