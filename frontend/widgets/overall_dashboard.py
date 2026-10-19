from PyQt5.QtWidgets import (
    QBoxLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from components.banner_4 import Banner4
from components.graph import GrowthCard
from components.employee_activity import EmployeeActivity
from components.custom_table import CustomTable
from components.status_badge import StatusBadge
from components.donut_card import DonutChartCard
from components.style_constants import (
    COLOR_BORDER,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    FONT_FAMILY,
)

CARD_MIN_HEIGHT = 300
STACK_ROWS_BELOW = 1000
BANNERS_2COL_BELOW = 880

class Dashboard(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("dashboard")

        self.initUi()
        self.setStylesheet()

        self.load_growth(
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            [18, 26, 34, 27, 49, 65, 75, 60, 0, 0, 13, 0],
        )
        self.load_sample_activities()

    def _make_card(self, object_name):
        card = QFrame()
        card.setObjectName(object_name)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        card.setMinimumHeight(CARD_MIN_HEIGHT)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)
        return card, layout

    def initUi(self):
        main_layout = QHBoxLayout(self)

        container_widget = QWidget()
        container_widget.setObjectName("container_widget")
        main_layout.addWidget(container_widget)

        content = QVBoxLayout(container_widget)
        content.setSpacing(14)

        header_widget = QWidget()
        header_row = QHBoxLayout(header_widget)
        header_row.setSpacing(12)

        icon = QLabel()
        icon.setFixedSize(50, 50)
        pixmap = QPixmap("resources/admin.svg")
        icon.setPixmap(
            pixmap.scaled(49, 49, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        header = QLabel("Dashboard")
        header.setObjectName("header")
        label = QLabel("Overview of the system.")
        label.setObjectName("label")
        text_col.addWidget(header)
        text_col.addWidget(label)

        header_row.addWidget(icon)
        header_row.addLayout(text_col)
        header_row.addStretch()
        header_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        content.addWidget(header_widget)

        self.banner_total_actions = Banner4(
            "resources/total_chamas.svg", "0", "Total Chamas"
        )
        self.banner_employees = Banner4(
            "resources/employee.svg", "0", "Employees"
        )
        self.banner_chamas = Banner4(
            "resources/total_members.svg", "0", "Total Members"
        )
        self.banner_today = Banner4(
            "resources/portfolio.svg", "0", "Portfolio"
        )
        self._banners = [
            self.banner_total_actions,
            self.banner_employees,
            self.banner_chamas,
            self.banner_today,
        ]
        for banner in self._banners:
            banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.banner_grid = QGridLayout()
        self.banner_grid.setSpacing(12)
        self._banner_cols = 0
        self._reflow_banners(4)
        content.addLayout(self.banner_grid)

        self.card = GrowthCard("Chama Growth")
        self.card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.card.setMinimumHeight(CARD_MIN_HEIGHT)

        recent_activity, ra_layout = self._make_card("recent_activity")
        recent_header = QLabel("Recent Employee Activity")
        recent_header.setObjectName("header_1")

        activity_scroll = QScrollArea()
        activity_scroll.setObjectName("activity_scroll")
        activity_scroll.setWidgetResizable(True)
        activity_scroll.setFrameShape(QFrame.NoFrame)
        activity_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        activity_holder = QWidget()
        activity_holder.setObjectName("activity_holder")
        self.recent_activities_layout = QVBoxLayout(activity_holder)
        self.recent_activities_layout.setContentsMargins(0, 0, 0, 0)
        self.recent_activities_layout.setSpacing(0)
        self.recent_activities_layout.addStretch()
        activity_scroll.setWidget(activity_holder)

        ra_layout.addWidget(recent_header)
        ra_layout.addWidget(activity_scroll, 1)

        self.row_top = QBoxLayout(QBoxLayout.LeftToRight)
        self.row_top.setSpacing(16)
        self.row_top.addWidget(self.card)
        self.row_top.addWidget(recent_activity)

        recent_chamas, rc_layout = self._make_card("recent_chamas")
        recent_chama = QLabel("Recent Chamas")
        recent_chama.setObjectName("header_1")

        self.recent_chamas_table = CustomTable([
            {"header": "Chama Name", "type": "text", "key": "name"},
            {"header": "Facilitator", "type": "text", "key": "facilitator", "center": True},
            {"header": "Members", "type": "text", "key": "members", "center": True},
            {
                "header": "Status",
                "key": "status",
                "factory": lambda value, row: StatusBadge(value),
            },
        ], frameless=True)
        self.recent_chamas_table.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.recent_chamas_table.setMinimumHeight(150)

        rc_layout.addWidget(recent_chama)
        rc_layout.addWidget(self.recent_chamas_table, 1)

        self.card_chart = DonutChartCard(
            title="Chama Onboarding",
            center_caption="Chamas\nin Progress",
            data=[
                ("Draft",         5, "#7CB4F5"),
                ("Onboarding",    8, "#2F5BEA"),
                ("Configuration", 6, "#3ECF9A"),
                ("Review",        3, "#2BB5D8"),
                ("Activation",    2, "#F5B82E"),
            ],
        )
        self.card_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.card_chart.setMinimumHeight(CARD_MIN_HEIGHT)

        self.row_bottom = QBoxLayout(QBoxLayout.LeftToRight)
        self.row_bottom.setSpacing(16)
        self.row_bottom.addWidget(recent_chamas)
        self.row_bottom.addWidget(self.card_chart)

        self._set_stacked(self.row_top, False)
        self._set_stacked(self.row_bottom, False)

        scroll = QScrollArea()
        scroll.setObjectName("dashboard_scroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_content")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)
        scroll_layout.addLayout(self.row_top, 1)
        scroll_layout.addLayout(self.row_bottom, 1)
        scroll.setWidget(scroll_content)

        content.addWidget(scroll, 1)

    def _reflow_banners(self, columns):
        if columns == self._banner_cols:
            return
        self._banner_cols = columns

        while self.banner_grid.count():
            self.banner_grid.takeAt(0)
        for c in range(4):
            self.banner_grid.setColumnStretch(c, 0)

        for i, banner in enumerate(self._banners):
            self.banner_grid.addWidget(banner, i // columns, i % columns)
        for c in range(columns):
            self.banner_grid.setColumnStretch(c, 1)

    @staticmethod
    def _set_stacked(row, stacked):
        direction = QBoxLayout.TopToBottom if stacked else QBoxLayout.LeftToRight
        if row.direction() != direction:
            row.setDirection(direction)
        row.setStretch(0, 1 if stacked else 3)
        row.setStretch(1, 1 if stacked else 2)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = event.size().width()
        self._reflow_banners(4 if width >= BANNERS_2COL_BELOW else 2)
        stacked = width < STACK_ROWS_BELOW
        self._set_stacked(self.row_top, stacked)
        self._set_stacked(self.row_bottom, stacked)

    def load_growth(self, labels, values):
        self.card.set_data(labels, values)

    def load_onboarding(self, data):
        self.card_chart.set_data(data)

    def add_activity(self, name, activity, time_text, avatar_path=None):
        kwargs = {"avatar_path": avatar_path} if avatar_path else {}
        row = EmployeeActivity(name, activity, time_text, **kwargs)
        self.recent_activities_layout.insertWidget(
            self.recent_activities_layout.count() - 1, row
        )

    def clear_activities(self):
        while self.recent_activities_layout.count() > 1:
            item = self.recent_activities_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def load_sample_activities(self):
        samples = [
            ("Joshua Mochama", "Created new chama 'Mwangaza Women Group'", "2 hours ago"),
            ("Joshua Mochama", "Added 5 new members to 'Umoja Savings'", "5 hours ago"),
            ("Joshua Mochama", "Updated contribution schedule", "Yesterday"),
            ("Joshua Mochama", "Changed a member's role to Treasurer", "2 days ago"),
        ]
        for name, activity, when in samples:
            self.add_activity(name, activity, when)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container_widget{{
                border: 1px solid {COLOR_BORDER};
                background-color: #FFFFFF;
                border-radius: 10px;
            }}
            QWidget#scroll_content{{
                background-color: #FFFFFF;
            }}
            QWidget#activity_holder{{
                background-color: #FFFFFF;
            }}
            QScrollArea#dashboard_scroll, QScrollArea#activity_scroll{{
                border: none;
            }}
            QFrame#recent_activity, QFrame#recent_chamas{{
                border: 1px solid {COLOR_BORDER};
                background-color: #FFFFFF;
                border-radius: 16px;
            }}
            QLabel#header{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 22px;
                font-weight: 600;
            }}
            QLabel#header_1{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
                background: transparent;
                border: none;
            }}
            QLabel#label{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 14px;
            }}
            QScrollBar:vertical{{
                border: none;
                background: transparent;
                width: 10px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical{{
                background: #c4c4c4;
                border-radius: 5px;
                min-height: 24px;
            }}
            QScrollBar::handle:vertical:hover{{
                background: #a6a6a6;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical{{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{{
                background: none;
            }}
        """)
