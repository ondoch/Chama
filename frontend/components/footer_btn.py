from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QButtonGroup
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class FooterButton(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout(self)

        self.previous_btn = QPushButton()
        self.previous_btn.setIcon(QIcon("resources/arrow-left.svg"))
        self.previous_btn.setIconSize(QSize(15, 15))
        self.previous_btn.setFixedSize(30, 30)

        self.next_btn = QPushButton()
        self.next_btn.setIcon(QIcon("resources/arrow-right.svg"))
        self.next_btn.setIconSize(QSize(15, 15))
        self.next_btn.setFixedSize(30, 30)

        self.btn_1 = QPushButton("1")
        self.btn_1.setFixedSize(30, 30)

        self.btn_2 = QPushButton("2")
        self.btn_2.setFixedSize(30, 30)

        self.btn_3 = QPushButton("3")
        self.btn_3.setFixedSize(30, 30)

        self.page_group = QButtonGroup(self)
        self.page_group.setExclusive(True)
        for btn in (self.btn_1, self.btn_2, self.btn_3):
            btn.setCheckable(True)
            self.page_group.addButton(btn)

        self.btn_1.setChecked(True)

        main_layout.addWidget(self.previous_btn)
        main_layout.addWidget(self.btn_1)
        main_layout.addWidget(self.btn_2)
        main_layout.addWidget(self.btn_3)
        main_layout.addWidget(self.next_btn)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QPushButton {{
                border-radius: 5px;
                border: 1px solid #ccc;
                background-color: #f5f5f5;
            }}
            QPushButton:hover {{
                background-color: #e0e0e0;
            }}
            QPushButton:checked {{
                background-color: #4a90e2;
                color: white;
                border: 1px solid #357abd;
            }}
        """)