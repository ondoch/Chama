from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout
)
from PyQt5.QtCore import Qt
from components.footer_btn import FooterButton
from components.style_constants import (
    FONT_FAMILY
)

class Pagination(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Showing 1 to 5 of 12 groups")
        label.setObjectName("label")
        label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        page_nav = FooterButton()

        main_layout.addWidget(label, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        main_layout.addStretch()
        main_layout.addWidget(page_nav, alignment=Qt.AlignVCenter | Qt.AlignRight)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QLabel#label{{
                font-family: {FONT_FAMILY};
                font-size: 14px;
            }}
        """)