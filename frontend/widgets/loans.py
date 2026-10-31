from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)

class Loans(QFrame):
    def __init__(self):
        super().__init__()

        self.initUi()
        self.setStylesheet()

    def initUi(self):
        main_layout = QHBoxLayout(self)

        container = QWidget()
        container_layout = QVBoxLayout(container)

        main_layout.addWidget(container)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            
        """)
