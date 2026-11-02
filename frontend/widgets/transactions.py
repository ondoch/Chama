from PyQt5.QtWidgets import(
    QFrame,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from components.form_dropdown import FormDropdown
from components.search_input import SearchInput
from components.pagination import Pagination
from components.transactions_table import TransactionsTable
from components.style_constants import (
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
)

class Transactions(QFrame):
    def __init__(self):
        super().__init__()
        
        self.initUi()
        self.setStylesheet()

    def initUi(self):
        main_layout = QVBoxLayout(self)

        container_widget = QWidget()
        container_widget_layout = QVBoxLayout(container_widget)

        header_widget = QWidget()
        header_widget_layout = QHBoxLayout(header_widget)
        header_widget_layout.setContentsMargins(20, 0, 0, 0)

        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_widget_layout.setSpacing(0)

        header = QLabel("Transactions")
        header.setObjectName("header")
        label = QLabel("View all chama transactions.")
        label.setObjectName("label")

        header_layout.addWidget(header)
        header_layout.addWidget(label)
        header_widget_layout.addLayout(header_layout)

        search_widget = QWidget()
        search_widget_layout = QHBoxLayout(search_widget)

        self.search = SearchInput("Search...")

        label_1 = QLabel("Filter by type:")
        label_1.setObjectName("label")
        self.types = FormDropdown(
            "All",
            [
                "Active",
                "Contribution",
                "Loan Repayment",
                "Loan Disbursement",
                "Cycle Disbursement",
                "Share Disbursement",
                "Other"
            ],
            height=40,
            icon_path="resources/down_arrow.svg",
        )
        search_widget_layout.addWidget(self.search, alignment=Qt.AlignRight | Qt.AlignVCenter)
        search_widget_layout.addWidget(label_1, alignment=Qt.AlignRight | Qt.AlignVCenter)
        search_widget_layout.addWidget(self.types, alignment=Qt.AlignRight | Qt.AlignVCenter)

        top_row_widget = QWidget()
        top_row_layout = QHBoxLayout(top_row_widget)
        top_row_layout.setContentsMargins(0, 0, 0, 0)

        top_row_layout.addWidget(header_widget, alignment=Qt.AlignLeft)
        top_row_layout.addStretch()
        top_row_layout.addWidget(
            search_widget, alignment=Qt.AlignRight | Qt.AlignVCenter
        )

        container_widget_layout.addWidget(top_row_widget)

        self.transaction_table = TransactionsTable()
        container_widget_layout.addWidget(self.transaction_table)

        footer = Pagination()
        container_widget_layout.addWidget(footer)

        main_layout.addWidget(container_widget)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QLabel#filter_label{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 13px;
            }}
        """)
