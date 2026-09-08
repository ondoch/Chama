from PyQt5.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QWidget
)

from PyQt5.QtCore import Qt

from components.container_1 import Container_1
from components.container_2 import Container_2
from components.container_3 import Container_3

class Widget4(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setAlignment(Qt.AlignCenter)

        chama_management = Container_1()
        member_management = Container_2()
        system_access = Container_3()

        container_layout.addWidget(chama_management)
        container_layout.addWidget(member_management)
        container_layout.addWidget(system_access)

        main_layout.addWidget(container_widget)

        self.setLayout(main_layout)
