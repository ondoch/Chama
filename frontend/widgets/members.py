from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtCore import Qt

from components.reports_members import ReportsMembersTable
from components.pagination import Pagination
from components.member_summary import MemberSummary

from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    FONT_FAMILY,
    COLOR_BORDER,
    COLOR_TEXT_MUTED
)

class Members(QFrame):
    def __init__(self):
        super().__init__()

        self.initUi()
        self.setStylesheet()

    def initUi(self):
        main_layout = QHBoxLayout(self)

        container = QWidget()
        container_layout = QVBoxLayout(container)

        header_layout = QVBoxLayout()

        header = QLabel("Members")
        header.setObjectName("header")
        header_1 = QLabel("View members of the chama")
        header_1.setObjectName("label")

        header_layout.addWidget(header)
        header_layout.addWidget(header_1)

        container_1 = QWidget()
        container_1_layout = QHBoxLayout(container_1)

        table_layout = QVBoxLayout()

        table = ReportsMembersTable()
        footer = Pagination()
        table_layout.addWidget(table)
        table_layout.addWidget(footer, alignment=Qt.AlignBottom)

        summary = MemberSummary()

        container_1_layout.addLayout(table_layout)
        container_1_layout.addWidget(summary)

        container_1_layout.setContentsMargins(1,5,5,5)
        container_1_layout.setSpacing(10)

        container_layout.addLayout(header_layout)
        container_layout.addWidget(container_1)

        main_layout.addWidget(container)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QLabel#header{{
                font-family: {FONT_FAMILY};
                color: {COLOR_TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
            QLabel#label{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 16px;
            }}
        """)
