from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from components.banner_4 import Banner4
from widgets.all_loans import AllLoans
from widgets.pending_approval import PendingApproval
from widgets.active_loans import ActiveLoans
from widgets.repaid_loans import RepaidLoans
from components.pagination import Pagination
from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER,
    COLOR_SIDEBAR_BG,
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

        header_container = QWidget()
        header_container_layout = QVBoxLayout(header_container)

        header = QLabel("Loans")
        header.setObjectName("header")
        sub_header = QLabel("Manage chama loans, approvals and repayments")
        sub_header.setObjectName("sub_header")

        header_container_layout.addWidget(header)
        header_container_layout.addWidget(sub_header)

        banner_layout = QHBoxLayout()
        banner_layout.setContentsMargins(0, 10, 0, 0)

        self.banner_total_contributions = Banner4(
            "resources/total_chamas.svg",
            "KES 210,000",
            "Total Loans Disbursed",
            "8 loans"
        )
        self.banner_total_loans = Banner4(
            "resources/employee.svg",
            "KES 165,000",
            "Outstanding Loans",
            "5 loans"
        )
        self.banner_members = Banner4(
            "resources/total_members.svg",
            "0",
            "Repaid Loans",
            "3 loans"
        )
        self.banner_duration = Banner4(
            "resources/portfolio.svg",
            "5",
            "Active Loans",
            "of 8 total"
        )

        banner_layout.addWidget(self.banner_total_contributions)
        banner_layout.addWidget(self.banner_total_loans)
        banner_layout.addWidget(self.banner_members)
        banner_layout.addWidget(self.banner_duration)

        container_layout.addWidget(header_container)
        container_layout.addLayout(banner_layout)
        container_layout.addWidget(self.build_tabs(), stretch=1)

        footer = Pagination()
        container_layout.addWidget(footer, alignment=Qt.AlignBottom)

        main_layout.addWidget(container)

    def build_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.setObjectName("report_tabs")
        self.tabs.setDocumentMode(True)

        tab_bar = self.tabs.tabBar()
        tab_bar.setExpanding(False)
        tab_bar.setDrawBase(False)
        tab_bar.setCursor(Qt.PointingHandCursor)
        tab_bar.setElideMode(Qt.ElideNone)
        tab_bar.setUsesScrollButtons(False)

        tab_font = QFont(tab_bar.font())
        tab_font.setPixelSize(14)
        tab_font.setWeight(QFont.DemiBold)
        tab_bar.setFont(tab_font)

        self.all_loans = AllLoans()
        self.pending_approval = PendingApproval()
        self.active_loans = ActiveLoans()
        self.repaid_loans = RepaidLoans()
        pages = [
            ("All Loans(15)", self.all_loans),
            ("Pending Approval(2)", self.pending_approval),
            ("Active Loans(8)", self.active_loans),
            ("Repaid Loans(5)", self.repaid_loans),
        ]

        self.pages = {}
        for title, page in pages:
            self.tabs.addTab(page, title)
            self.pages[title] = page

        return self.tabs

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QLabel#header{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 20px;
                font-weight: 600;
            }}
            QLabel#sub_header{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 16px;
            }}
            QTabWidget#report_tabs::pane{{
                border: none;
                border-top: 1px solid {COLOR_BORDER};
                background: transparent;
            }}
            QTabWidget#report_tabs QTabBar{{
                background: transparent;
            }}
            QTabWidget#report_tabs QTabBar::tab{{
                font-family: {FONT_FAMILY};
                font-size: 14px;
                font-weight: 600;
                color: {COLOR_TEXT_MUTED};
                background: transparent;
                border: none;
                border-bottom: 2px solid transparent;
                padding: 10px 24px;
                margin-right: 6px;
                min-width: 80px;
            }}
            QTabWidget#report_tabs QTabBar::tab:hover{{
                color: {COLOR_TEXT_PRIMARY};
            }}
            QTabWidget#report_tabs QTabBar::tab:selected{{
                color: {COLOR_SIDEBAR_BG};
                border-bottom: 2px solid {COLOR_SIDEBAR_BG};
            }}
        """)
