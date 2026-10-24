from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QSizePolicy,
    QHBoxLayout,
    QVBoxLayout
)

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from components.banner_4 import Banner4
from components.search_input import SearchInput
from components.form_dropdown import FormDropdown
from components.pagination import Pagination
from components.reports_table import ReportsTable
from components.status_badge import StatusBadge
from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER,
)

from modals.reports_information import ReportModal

class ReportsDashboard(QFrame):
    def __init__(self):
        super().__init__()

        self.initUi()
        self.setStylesheet()
        self.table.load_sample_data()

    def initUi(self):
        main_layout = QHBoxLayout(self)

        container_widget = QWidget()
        container_widget.setObjectName("container_widget")
        container_widget_layout = QVBoxLayout(container_widget)
        main_layout.addWidget(container_widget)

        header_widget = QWidget()
        header_widget_layout = QHBoxLayout(header_widget)
        header_widget_layout.setContentsMargins(20, 0, 0, 0)

        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(10, 0, 0, 0)
        header_widget_layout.setSpacing(0)

        icon = QLabel()
        icon.setFixedSize(50, 50)
        pixmap = QPixmap("resources/group_1.svg")
        icon.setPixmap(
            pixmap.scaled(49, 49, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        header = QLabel("All Chamas Report")
        header.setObjectName("header")
        label = QLabel("Overview of all chamas and performance.")
        label.setObjectName("label")

        header_layout.addWidget(header)
        header_layout.addWidget(label)
        header_widget_layout.addWidget(icon)
        header_widget_layout.addLayout(header_layout)

        top_row_widget = QWidget()
        top_row_layout = QHBoxLayout(top_row_widget)
        top_row_layout.setContentsMargins(0, 0, 0, 0)

        top_row_layout.addWidget(header_widget, alignment=Qt.AlignLeft)

        banner_layout = QHBoxLayout()
        banner_layout.setSpacing(12)

        left, top, right, bottom = banner_layout.getContentsMargins()
        banner_layout.setContentsMargins(left, 10, right, bottom)

        self.banner_total_chamas = Banner4(
            "resources/chamas.svg",
            "0",
            "Total Chamas",
            "0 Active"
        )
        self.banner_total_members = Banner4(
            "resources/people.svg",
            "0",
            "Total Members",
            "Across all"
        )
        self.banner_total_contribution = Banner4(
            "resources/inactive_users.svg",
            "0",
            "Total Contributions",
            "12% vs. the previous period",
        )
        self.banner_total_loans = Banner4(
            "resources/inactive_users.svg",
            "0",
            "Total loans disbursed",
            "18% vs. the previous period",
        )
        self.banner_active_cycles = Banner4(
            "resources/leader_1.svg",
            "0",
            "Active Cycles",
            "Current cycle: jan 2025-Dec 2025",
        )

        banner_layout.addWidget(self.banner_total_chamas, stretch=1)
        banner_layout.addWidget(self.banner_total_members, stretch=1)
        banner_layout.addWidget(self.banner_total_contribution, stretch=1)
        banner_layout.addWidget(self.banner_total_loans, stretch=1)
        banner_layout.addWidget(self.banner_active_cycles, stretch=1)

        search_widget = QWidget()
        search_widget_layout = QHBoxLayout(search_widget)

        self.search = SearchInput("Search...")
        self.search.setMaximumWidth(300)

        self.status_dropdown = FormDropdown(
            "All",
            ["Active", "Inactive", "Onboarding"],
            height=40,
            icon_path="resources/down_arrow.svg",
        )
        self.cycle_dropdown = FormDropdown(
            "All",
            ["Active", "Inactive", "Onboarding"],
            height=40,
            icon_path="resources/down_arrow.svg",
        )
        search_widget_layout.addWidget(self.search)
        search_widget_layout.addStretch()
        search_widget_layout.addWidget(self.status_dropdown)
        search_widget_layout.addWidget(self.cycle_dropdown)

        self.table = ReportsTable(on_view = self.openReportModal)

        container_widget_layout.addWidget(top_row_widget)
        container_widget_layout.addLayout(banner_layout)
        container_widget_layout.addWidget(search_widget)
        container_widget_layout.addWidget(self.table, stretch=1)

        footer = Pagination()
        container_widget_layout.addWidget(footer, alignment=Qt.AlignBottom)

    def openReportModal(self, row_data):
        modal = ReportModal(row_data=row_data, parent=self)
        modal.setWindowTitle("Chama Report")
        modal.exec_()

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container_widget{{
                border: 1px solid {COLOR_BORDER};
                background-color: #FFFFFF;
                border-radius: 10px;
            }}
            QLabel#header{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 20px;
                font-weight: 600;
            }}
            QLabel#label{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 16px;
            }}
        """)
