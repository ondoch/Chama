from PyQt5.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QWidget
)
from PyQt5.QtCore import Qt
from components.style_constants import COLOR_BORDER
from components.header import Header
from components.checkbox import CheckBox
class Container_1(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        container = QWidget()
        container.setFixedWidth(350)
        container.setObjectName("chama_container")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(0)

        header = Header("Chama Management")
        create_chama = CheckBox("Create Chama")
        view_chama = CheckBox("View Chama Details")
        update_chama = CheckBox("Update Chama Information")
        chama_settings = CheckBox("Configure Chama Settings")

        container_layout.addWidget(header)
        container_layout.addWidget(create_chama)
        container_layout.addWidget(view_chama)
        container_layout.addWidget(update_chama)
        container_layout.addWidget(chama_settings)

        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#chama_container{{
                background: #FFFFFF;
                border: 1px solid {COLOR_BORDER};
                border-radius: 5px;
            }}
        """)
