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
from components.form_dropdown import FormDropdown
from components.onboarding_table import OnboardingTable
from components.employee_activity import EmployeeActivity
from components.donut_card import DonutChartCard
from components.search_input import SearchInput
from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER,
)

TABLE_MIN_HEIGHT = 320
CARD_MIN_HEIGHT = 280
STACK_BODY_BELOW = 1000
BANNERS_2COL_BELOW = 880
SIDE_CARDS_ROW_FROM = 760
FILTERS_1COL_BELOW = 640

SAMPLE_CHAMAS = [
    {"chama_name": "Tumaini Group",      "facilitator": "Mary Wanjiku", "progress": 80,
     "status": "Rules",     "started": "20 Aug 2026"},
    {"chama_name": "Jirani Chama",       "facilitator": "Jane Njeri",   "progress": 60,
     "status": "Officials", "started": "18 Aug 2026"},
    {"chama_name": "Upendo Women",       "facilitator": "Mary Wanjiku", "progress": 90,
     "status": "Review",    "started": "16 Aug 2026"},
    {"chama_name": "Baraka Investment",  "facilitator": "Peter Otieno", "progress": 40,
     "status": "Members",   "started": "14 Aug 2026"},
    {"chama_name": "Mwangaza Women",     "facilitator": "Jane Njeri",   "progress": 100,
     "status": "Active",    "started": "10 Aug 2026"},
    {"chama_name": "Umoja Savings",      "facilitator": "Peter Otieno", "progress": 25,
     "status": "Rules",     "started": "08 Aug 2026"},
    {"chama_name": "Jamii Traders",      "facilitator": "Mary Wanjiku", "progress": 70,
     "status": "Officials", "started": "05 Aug 2026"},
    {"chama_name": "Tumaini Youth",      "facilitator": "Jane Njeri",   "progress": 55,
     "status": "Members",   "started": "02 Aug 2026"},
]


class Onboarding(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("onboarding")

        self.initUi()
        self.setStylesheet()

        self.load_sample_chamas()
        self.load_sample_activities()

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
        pixmap = QPixmap("resources/onboarding_1.svg")
        icon.setPixmap(
            pixmap.scaled(49, 49, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        header = QLabel("Onboarding")
        header.setObjectName("header")
        label = QLabel("Track chama setup and identify incomplete onboarding.")
        label.setObjectName("label")
        label.setWordWrap(True)
        text_col.addWidget(header)
        text_col.addWidget(label)

        header_row.addWidget(icon)
        header_row.addLayout(text_col, 1)
        header_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        content.addWidget(header_widget)

        self.banner_total_chamas = Banner4(
            "resources/chamas.svg",
            "0",
            "In progress",
            "Chamas being set up"
        )
        self.banner_members = Banner4(
            "resources/people.svg",
            "0",
            "Almost done",
            "Ready for activation"
        )
        self.banner_pending = Banner4(
            "resources/inactive_users.svg",
            "0",
            "Waiting",
            "Pending information",
        )
        self.banner_officials = Banner4(
            "resources/leader_1.svg",
            "0",
            "Needs attention",
            "Requires intervention",
        )
        self._banners = [
            self.banner_total_chamas,
            self.banner_members,
            self.banner_pending,
            self.banner_officials,
        ]
        for banner in self._banners:
            banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.banner_grid = QGridLayout()
        self.banner_grid.setSpacing(12)
        self._banner_cols = 0
        self._reflow_banners(4)
        content.addLayout(self.banner_grid)

        self.search = SearchInput("Search...")
        self.search.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.facilitators_dropdown = FormDropdown(
            "All",
            ["Active", "Inactive", "Onboarding"],
            height=40,
            icon_path="resources/down_arrow.svg",
        )
        self.progress_dropdown = FormDropdown(
            "All",
            ["Active", "Inactive", "Onboarding"],
            height=40,
            icon_path="resources/down_arrow.svg",
        )
        self.status_dropdown = FormDropdown(
            "All",
            ["Active", "Inactive", "Onboarding"],
            height=40,
            icon_path="resources/down_arrow.svg",
        )

        self._filter_boxes = [
            self._make_filter("Facilitator", self.facilitators_dropdown),
            self._make_filter("Progress", self.progress_dropdown),
            self._make_filter("Status", self.status_dropdown),
        ]
        self.filter_grid = QGridLayout()
        self.filter_grid.setContentsMargins(0, 0, 0, 0)
        self.filter_grid.setHorizontalSpacing(12)
        self.filter_grid.setVerticalSpacing(8)
        self._filter_cols = 0
        self._reflow_filters(3)

        self.onboarding_chamas_table = OnboardingTable()
        self.onboarding_chamas_table.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.onboarding_chamas_table.setMinimumHeight(TABLE_MIN_HEIGHT)

        left_col = QVBoxLayout()
        left_col.setContentsMargins(0, 0, 0, 0)
        left_col.setSpacing(12)
        left_col.addWidget(self.search)
        left_col.addLayout(self.filter_grid)
        left_col.addWidget(self.onboarding_chamas_table, 1)

        self.card_chart = DonutChartCard(
            title="Chama Onboarding",
            center_caption="Total Chamas",
            data=[
                ("Completed",       3, "#05FA80"),
                ("In progress",     2, "#0066FF"),
                ("Almost done",     4, "#FFD900"),
                ("Needs attention", 1, "#FF002B"),
                ("Waiting",         1, "#8AA2C3"),
            ],
        )
        self.card_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.card_chart.setMinimumHeight(CARD_MIN_HEIGHT)

        recent_onboarding = QFrame()
        recent_onboarding.setObjectName("recent_onboarding")
        recent_onboarding.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        recent_onboarding.setMinimumHeight(CARD_MIN_HEIGHT)
        ro_layout = QVBoxLayout(recent_onboarding)
        ro_layout.setContentsMargins(18, 16, 18, 16)
        ro_layout.setSpacing(10)

        ro_title = QLabel("Recent Onboarding Activities")
        ro_title.setObjectName("card_title")

        activity_scroll = QScrollArea()
        activity_scroll.setObjectName("activity_scroll")
        activity_scroll.setWidgetResizable(True)
        activity_scroll.setFrameShape(QFrame.NoFrame)
        activity_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        activity_holder = QWidget()
        activity_holder.setObjectName("activity_holder")
        self.recent_onboarding_layout = QVBoxLayout(activity_holder)
        self.recent_onboarding_layout.setContentsMargins(0, 0, 0, 0)
        self.recent_onboarding_layout.setSpacing(0)
        self.recent_onboarding_layout.addStretch()
        activity_scroll.setWidget(activity_holder)

        ro_layout.addWidget(ro_title)
        ro_layout.addWidget(activity_scroll, 1)

        self.right_col = QBoxLayout(QBoxLayout.TopToBottom)
        self.right_col.setContentsMargins(0, 0, 0, 0)
        self.right_col.setSpacing(16)
        self.right_col.addWidget(self.card_chart, 1)
        self.right_col.addWidget(recent_onboarding, 1)

        self.body = QBoxLayout(QBoxLayout.LeftToRight)
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.setSpacing(16)
        self.body.addLayout(left_col)
        self.body.addLayout(self.right_col)
        self._set_body_stacked(False)

        scroll = QScrollArea()
        scroll.setObjectName("onboarding_scroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_content")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 6, 0)     # room for the scrollbar
        scroll_layout.addLayout(self.body)
        scroll.setWidget(scroll_content)

        content.addWidget(scroll, 1)

    def _make_filter(self, text, dropdown):
        box = QWidget()
        layout = QVBoxLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        label = QLabel(text)
        label.setObjectName("filter_label")
        dropdown.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(label)
        layout.addWidget(dropdown)
        return box

    @staticmethod
    def _fill_grid(grid, widgets, columns):
        while grid.count():
            grid.takeAt(0)
        for c in range(len(widgets)):
            grid.setColumnStretch(c, 0)
        for i, widget in enumerate(widgets):
            grid.addWidget(widget, i // columns, i % columns)
        for c in range(columns):
            grid.setColumnStretch(c, 1)

    def _reflow_banners(self, columns):
        if columns != self._banner_cols:
            self._banner_cols = columns
            self._fill_grid(self.banner_grid, self._banners, columns)

    def _banners_need_width(self):
        banners = sum(b.minimumSizeHint().width() for b in self._banners)
        return max(BANNERS_2COL_BELOW, banners + 3 * 12 + 80)

    def _reflow_filters(self, columns):
        if columns != self._filter_cols:
            self._filter_cols = columns
            self._fill_grid(self.filter_grid, self._filter_boxes, columns)

    def _set_body_stacked(self, stacked):
        direction = QBoxLayout.TopToBottom if stacked else QBoxLayout.LeftToRight
        if self.body.direction() != direction:
            self.body.setDirection(direction)
        self.body.setStretch(0, 1 if stacked else 3)
        self.body.setStretch(1, 1 if stacked else 2)

    def _set_right_side_by_side(self, side_by_side):
        direction = QBoxLayout.LeftToRight if side_by_side else QBoxLayout.TopToBottom
        if self.right_col.direction() != direction:
            self.right_col.setDirection(direction)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = event.size().width()
        stacked = width < STACK_BODY_BELOW
        self._reflow_banners(4 if width >= self._banners_need_width() else 2)
        self._reflow_filters(3 if width >= FILTERS_1COL_BELOW else 1)
        self._set_body_stacked(stacked)
        self._set_right_side_by_side(stacked and width >= SIDE_CARDS_ROW_FROM)

    def load_chamas(self, rows):
        self.onboarding_chamas_table.populate(rows)

    def load_sample_chamas(self):
        self.load_chamas(SAMPLE_CHAMAS)

    def load_onboarding(self, data):
        self.card_chart.set_data(data)

    def add_activity(self, name, activity, time_text, avatar_path=None):
        kwargs = {"avatar_path": avatar_path} if avatar_path else {}
        row = EmployeeActivity(name, activity, time_text, **kwargs)
        self.recent_onboarding_layout.insertWidget(
            self.recent_onboarding_layout.count() - 1, row
        )

    def clear_activities(self):
        while self.recent_onboarding_layout.count() > 1:
            item = self.recent_onboarding_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def load_sample_activities(self):
        samples = [
            ("Joshua Mochama", "Started onboarding 'Mwangaza Women Group'", "2 hours ago"),
            ("Joshua Mochama", "Moved 'Umoja Savings' to Review", "5 hours ago"),
            ("Joshua Mochama", "Completed configuration for 'Tumaini Youth'", "Yesterday"),
            ("Joshua Mochama", "Activated 'Jamii Traders'", "2 days ago"),
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
            QWidget#scroll_content, QWidget#activity_holder{{
                background-color: #FFFFFF;
            }}
            QScrollArea#onboarding_scroll, QScrollArea#activity_scroll{{
                border: none;
            }}
            QFrame#recent_onboarding{{
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
            QLabel#label{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 14px;
            }}
            QLabel#card_title{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
                background: transparent;
                border: none;
            }}
            QLabel#filter_label{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 13px;
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
