from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtCore import Qt

from components.banner_4 import Banner4
from components.donut_card import DonutChartCard
from components.bar_chart import TrendBarChart
from components.summary_card import SummaryCard
from components.style_constants import COLOR_BORDER
from components.recent_contribution_table import RecentContributionTable
from components.recent_loans_table import RecentLoansTable

from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER,
)

CARD_MIN_HEIGHT = 280
CHART_ROW_MIN_HEIGHT = 320
SUMMARY_ROW_MIN_HEIGHT = 240


class Overview(QFrame):
    def __init__(self):
        super().__init__()

        self.initUi()
        self.setStylesheet()

    def initUi(self):
        main_layout = QHBoxLayout(self)

        container_widget = QWidget()
        container_widget.setObjectName("container_widget")
        container_widget_layout = QVBoxLayout(container_widget)

        container_widget_layout.addLayout(self.build_banners())

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_content")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 6, 0)
        scroll_layout.setSpacing(12)

        scroll_layout.addWidget(self.build_chart_row(), stretch=3)
        scroll_layout.addWidget(self.build_summary_row(), stretch=2)
        scroll_layout.addWidget(self.build_table_row(), stretch=2)

        self.scroll_area.setWidget(scroll_content)
        container_widget_layout.addWidget(self.scroll_area, stretch=1)

        main_layout.addWidget(container_widget)

    def build_banners(self):
        banner_layout = QHBoxLayout()
        banner_layout.setSpacing(12)

        left, top, right, bottom = banner_layout.getContentsMargins()
        banner_layout.setContentsMargins(left, 10, right, bottom)

        self.banner_total_chamas = Banner4(
            "resources/chamas.svg", "0", "Total Chamas", "0 Active"
        )
        self.banner_members = Banner4(
            "resources/people.svg", "0", "Members", "Across all"
        )
        self.banner_pending = Banner4(
            "resources/inactive_users.svg",
            "0",
            "Pending Approvals",
            "Waiting for confirmation",
        )
        self.banner_officials = Banner4(
            "resources/leader_1.svg",
            "0",
            "Chama Officials",
            "Across all chamas",
        )

        banner_layout.addWidget(self.banner_total_chamas, stretch=1)
        banner_layout.addWidget(self.banner_members, stretch=1)
        banner_layout.addWidget(self.banner_pending, stretch=1)
        banner_layout.addWidget(self.banner_officials, stretch=1)

        return banner_layout

    def build_chart_row(self):
        row = QWidget()
        row.setMinimumHeight(CHART_ROW_MIN_HEIGHT)
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        self.trend_chart = TrendBarChart("Contribution Trend")

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_contributions = [65000, 65000, 86000, 89000, 104000, 99000,
                                 106000, 118000, 93000, 111000, None, None]
        targets = [100000] * 10 + [109000, 140000]
        self.trend_chart.set_data(months, monthly_contributions, targets)

        self.card_chart = DonutChartCard(
            title="Chama Onboarding",
            center_caption="Total Cycles",
            data=[
                ("Completed", 4, "#05FA80"),
                ("Remaining", 1, "#0066FF"),
            ],
        )
        self.card_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.card_chart.setMinimumHeight(CARD_MIN_HEIGHT)

        row_layout.addWidget(self.trend_chart)
        row_layout.addWidget(self.card_chart)

        return row

    def build_summary_row(self):
        row = QWidget()
        row.setMinimumHeight(SUMMARY_ROW_MIN_HEIGHT)
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        self.contribution_summary = SummaryCard(
            title="Contribution Summary",
            top_left=("Total contributions", "KES 320,000"),
            bottom_left=("Member contribution", "KES 3,000"),
            top_right=("Expected (by Dec)", "KES 384,000"),
            highlight=("Pending", "KES 64,000"),
        )

        self.loan_summary = SummaryCard(
            title="Loan Summary",
            top_left=("Total loans disbursed", "KES 210,000"),
            bottom_left=("Active loans", "7"),
            top_right=("Total repayments", "KES 165,000"),
            highlight=("Pending repayments", "KES 45,000"),
        )

        row_layout.addWidget(self.contribution_summary)
        row_layout.addWidget(self.loan_summary)

        return row

    def build_table_row(self):
        row = QWidget()
        row.setMinimumHeight(SUMMARY_ROW_MIN_HEIGHT)
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        table_1 = QVBoxLayout()
        table_2 = QVBoxLayout()

        label = QLabel("Recent Contributions")
        label.setObjectName("header")
        self.contributions_table = RecentContributionTable()
        self.contributions_table.load_sample_data()
        table_1.addWidget(label)
        table_1.addWidget(self.contributions_table)

        label = QLabel("Recent Loans")
        label.setObjectName("header")
        self.loans_table = RecentLoansTable()
        self.loans_table.load_sample_data()
        table_2.addWidget(label)
        table_2.addWidget(self.loans_table)
        
        row_layout.addLayout(table_1)
        row_layout.addLayout(table_2)

        return row

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget{{
                border: none;
            }}
            QScrollArea#scroll_area{{
                background: transparent;
                border: none;
            }}
            QScrollArea#scroll_area > QWidget > QWidget#scroll_content{{
                background: transparent;
            }}
            QScrollBar:vertical{{
                background: transparent;
                width: 8px;
                margin: 2px 0 2px 0;
            }}
            QScrollBar::handle:vertical{{
                background: {COLOR_BORDER};
                border-radius: 4px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover{{
                background: #C3C9D2;
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical{{
                height: 0px;
            }}
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical{{
                background: transparent;
            }}
            QLabel#header{{
                font-family: {FONT_FAMILY};
                color: {COLOR_TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
        """)
