from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QProgressBar,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout
)

from components.banner_4 import Banner4
from components.timetable import Timetable
from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER,
    COLOR_SIDEBAR_BG,
)

COLUMNS = 5

# (name, amount, date, completed) -> 6 completed, 4 remaining
TIMETABLE_DATA = [
    ("Peter Mwangi",  "KES 40,000", "12/1/2026", True),
    ("Mary Wanjiku",  "KES 40,000", "12/2/2026", True),
    ("John Otieno",   "KES 40,000", "12/3/2026", True),
    ("Grace Akinyi",  "KES 40,000", "12/4/2026", True),
    ("David Kamau",   "KES 40,000", "12/5/2026", True),
    ("Lucy Njeri",    "KES 40,000", "12/6/2026", True),
    ("Samuel Kiptoo", "KES 40,000", "12/7/2026", False),
    ("Esther Atieno", "KES 40,000", "12/8/2026", False),
    ("James Mutua",   "KES 40,000", "12/9/2026", False),
    ("Faith Chebet",  "KES 40,000", "12/10/2026", False),
]


class Cycle(QFrame):
    def __init__(self):
        super().__init__()

        self.initUi()
        self.setStylesheet()
        self.load_timetable(TIMETABLE_DATA)

    def initUi(self):
        main_layout = QHBoxLayout(self)

        container = QWidget()
        container_layout = QVBoxLayout(container)

        header_container = QWidget()
        header_container_layout = QVBoxLayout(header_container)

        header = QLabel("Cycle")
        header.setObjectName("header")
        sub_header = QLabel("View chama cycles, targets and progress.")
        sub_header.setObjectName("sub_header")

        header_container_layout.addWidget(header)
        header_container_layout.addWidget(sub_header)

        container_1 = QWidget()
        container_1.setObjectName("container")
        container_1_layout = QVBoxLayout(container_1)
        container_1_layout.setContentsMargins(20, 16, 20, 20)
        container_1_layout.setSpacing(6)

        label_1 = QLabel("Current Cycle")
        label_1.setObjectName("label_1")

        self.cycle = QLabel("Jan 2025 - Dec 2025")
        self.cycle.setObjectName("cycle")

        progress_layout = QVBoxLayout()
        progress_layout.setContentsMargins(0, 10, 0, 0)
        progress_layout.setSpacing(8)

        percentage_row = QHBoxLayout()
        percentage_row.setContentsMargins(0, 0, 0, 0)

        progress_label = QLabel("Progress")
        progress_label.setObjectName("progress_label")

        self.percentage = QLabel("0% complete")
        self.percentage.setObjectName("percentage")

        percentage_row.addWidget(progress_label)
        percentage_row.addStretch()
        percentage_row.addWidget(self.percentage)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)

        progress_layout.addLayout(percentage_row)
        progress_layout.addWidget(self.progress_bar)

        banner_layout = QHBoxLayout()
        banner_layout.setContentsMargins(0, 10, 0, 0)

        self.banner_total_contributions = Banner4(
            "resources/total_chamas.svg", "0", "Total Contributions"
        )
        self.banner_total_loans = Banner4(
            "resources/employee.svg", "0", "Total loans disbursed"
        )
        self.banner_members = Banner4(
            "resources/total_members.svg", "0", "Total Members"
        )
        self.banner_duration = Banner4(
            "resources/portfolio.svg", "0", "Duration"
        )

        banner_layout.addWidget(self.banner_total_contributions)
        banner_layout.addWidget(self.banner_total_loans)
        banner_layout.addWidget(self.banner_members)
        banner_layout.addWidget(self.banner_duration)

        container_1_layout.addWidget(label_1)
        container_1_layout.addWidget(self.cycle)
        container_1_layout.addLayout(progress_layout)
        container_1_layout.addLayout(banner_layout)

        group_timetable = QLabel("Group Timetable")
        group_timetable.setObjectName("timetable")

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setHorizontalSpacing(12)
        self.grid_layout.setVerticalSpacing(12)
        for col in range(COLUMNS):
            self.grid_layout.setColumnStretch(col, 1)

        container_layout.addWidget(header_container)
        container_layout.addWidget(container_1)
        container_layout.addWidget(group_timetable)
        container_layout.addLayout(self.grid_layout)
        container_layout.addStretch()

        main_layout.addWidget(container)

    def load_timetable(self, data):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        completed_count = 0
        for index, (name, amount, date, completed) in enumerate(data):
            card = Timetable(name, amount, date, completed)
            row, col = divmod(index, COLUMNS)
            self.grid_layout.addWidget(card, row, col)
            if completed:
                completed_count += 1

        total = len(data)
        self.set_progress((completed_count / total) * 100 if total else 0)

    def set_progress(self, value):
        value = max(0, min(100, int(value)))
        self.progress_bar.setValue(value)
        self.percentage.setText(f"{value}% complete")

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QWidget#container{{
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
            QLabel#timetable{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 14px;
                font-weight: 500;
            }}
            QLabel#sub_header{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 16px;
            }}
            QLabel#label_1{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 14px;
                font-weight: 600;
            }}
            QLabel#cycle{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 15px;
                font-weight: 600;
            }}
            QLabel#progress_label{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 14px;
            }}
            QLabel#percentage{{
                font-family: {FONT_FAMILY};
                font-size: 14px;
            }}
            QProgressBar{{
                background-color: {COLOR_BORDER};
                border: none;
                border-radius: 5px;
            }}
            QProgressBar::chunk{{
                background-color: {COLOR_SIDEBAR_BG};
                border-radius: 5px;
            }}
        """)
