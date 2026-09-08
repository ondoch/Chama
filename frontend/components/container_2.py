from PyQt5.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QWidget
)
from PyQt5.QtCore import Qt
from components.style_constants import COLOR_BORDER
from components.header import Header
from components.checkbox import CheckBox
class Container_2(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        container = QWidget()
        container.setFixedWidth(350)
        container.setObjectName("member_container")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(0)

        header = Header("Member Management")
        add_members = CheckBox("Add Members")
        view_members = CheckBox("View Members")
        update_members = CheckBox("Update Member Information")
        remove_members = CheckBox("Remove Members")

        container_layout.addWidget(header)
        container_layout.addWidget(add_members)
        container_layout.addWidget(view_members)
        container_layout.addWidget(update_members)
        container_layout.addWidget(remove_members)

        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#member_container{{
                background: #FFFFFF;
                border: 1px solid {COLOR_BORDER};
                border-radius: 5px;
            }}
        """)
