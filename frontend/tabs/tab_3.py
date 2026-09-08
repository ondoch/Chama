from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout
)

from widgets.widget_5 import Widget5
from components.style_constants import COLOR_BORDER, COLOR_ACCENT_BLUE

class Tab3(QFrame):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout()

        widget_1 = Widget5()
        main_layout.addWidget(widget_1)

        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            
        """)
