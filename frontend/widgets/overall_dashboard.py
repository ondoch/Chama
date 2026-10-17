from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from components.banner_4 import Banner4
from components.graph import GrowthCard
from components.employee_activity import EmployeeActivity
from components.custom_table import CustomTable
from components.status_badge import StatusBadge
from components.style_constants import (
    COLOR_BORDER,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    FONT_FAMILY,
)


class Dashboard(QFrame):
    def __init__(self):
        super().__init__()

        self.initUi()
        self.setStylesheet()

        # temporary sample data - replace with real data later
        self.load_growth(
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"],
            [18, 26, 34, 27, 49, 65, 75, 60],
        )
        self.load_sample_activities()

    def initUi(self):
        main_layout = QHBoxLayout(self)

        container_widget = QWidget()
        container_widget.setObjectName("container_widget")
        container_widget_layout = QVBoxLayout(container_widget)

        # ---------- header ----------
        header_widget = QWidget()
        header_widget_layout = QHBoxLayout(header_widget)
        header_widget_layout.setContentsMargins(20, 0, 0, 0)
        header_widget_layout.setSpacing(0)

        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(10, 0, 0, 0)

        icon = QLabel()
        icon.setFixedSize(50, 50)
        pixmap = QPixmap("resources/security.svg")
        icon.setPixmap(
            pixmap.scaled(49, 49, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        header = QLabel("Dashboard")
        header.setObjectName("header")
        label = QLabel("Overview of the system.")
        label.setObjectName("label")

        header_layout.addWidget(header)
        header_layout.addWidget(label)
        header_widget_layout.addWidget(icon)
        header_widget_layout.addLayout(header_layout)

        top_row = QWidget()
        top_row_layout = QHBoxLayout(top_row)
        top_row_layout.setContentsMargins(0, 0, 0, 0)
        top_row_layout.addWidget(header_widget)

        # ---------- banners ----------
        banner_layout = QHBoxLayout()
        banner_layout.setSpacing(12)
        left, _, right, bottom = banner_layout.getContentsMargins()
        banner_layout.setContentsMargins(left, 10, right, bottom)

        self.banner_total_actions = Banner4(
            "resources/total_actions.svg", "0", "Total Actions"
        )
        self.banner_employees = Banner4(
            "resources/audit_user.svg", "0", "Employees"
        )
        self.banner_chamas = Banner4(
            "resources/users_chama.svg", "0", "Chamas"
        )
        self.banner_today = Banner4(
            "resources/today.svg", "0", "Today"
        )

        top_row.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        for banner in (
            self.banner_total_actions,
            self.banner_employees,
            self.banner_chamas,
            self.banner_today,
        ):
            banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
            banner_layout.addWidget(banner, stretch=1)

        # ---------- row 1: growth chart + recent employee activity ----------
        self.card = GrowthCard("Chama Growth")
        self.card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        recent_activity = QWidget()
        recent_activity.setObjectName("recent_activity")
        recent_activity.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        recent_activity_layout = QVBoxLayout(recent_activity)

        recent_header = QLabel("Recent Employee Activity")
        recent_header.setObjectName("header_1")

        self.recent_activities_layout = QVBoxLayout()
        self.recent_activities_layout.setSpacing(0)

        recent_activity_layout.addWidget(recent_header)
        recent_activity_layout.addLayout(self.recent_activities_layout)
        recent_activity_layout.addStretch()

        container_1 = QWidget()
        container_1_layout = QHBoxLayout(container_1)
        container_1_layout.setContentsMargins(0, 0, 0, 0)
        container_1_layout.setSpacing(12)
        container_1_layout.addWidget(self.card, 1)
        container_1_layout.addWidget(recent_activity, 1)

        # ---------- row 2: recent chamas table ----------
        container_2 = QWidget()
        container_2.setObjectName("recent_chamas")
        container_2_layout = QVBoxLayout(container_2)
        container_2_layout.setContentsMargins(16, 12, 16, 12)

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
        ])
        # the table fills the card but must NOT dictate the window height
        self.recent_chamas_table.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.recent_chamas_table.setMinimumHeight(0)

        container_2_layout.addWidget(recent_chama)
        container_2_layout.addWidget(self.recent_chamas_table, 1)

        # ---------- make both rows exactly equal in height ----------
        # "Ignored" vertically = the content's preferred height is ignored, so
        # only the stretch factors (1 : 1) decide how the space is shared.
        for row in (container_1, container_2):
            row.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
            row.setMinimumHeight(220)

        # ---------- assemble ----------
        container_widget_layout.addWidget(top_row)
        container_widget_layout.addLayout(banner_layout)
        container_widget_layout.addWidget(container_1, 1)
        container_widget_layout.addWidget(container_2, 1)

        main_layout.addWidget(container_widget)

    # ---------- data helpers ----------
    def load_growth(self, labels, values):
        """labels: ['Jan', 'Feb', ...], values: [18, 26, ...]"""
        self.card.set_data(labels, values)

    def add_activity(self, name, activity, time_text, avatar_path=None):
        kwargs = {"avatar_path": avatar_path} if avatar_path else {}
        row = EmployeeActivity(name, activity, time_text, **kwargs)
        self.recent_activities_layout.addWidget(row)

    def clear_activities(self):
        while self.recent_activities_layout.count():
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
            QWidget#recent_activity, QWidget#recent_chamas{{
                border: 1px solid {COLOR_BORDER};
                background-color: #FFFFFF;
                border-radius: 16px;
            }}
            QLabel#header{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 20px;
                font-weight: 600;
            }}
            QLabel#header_1{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
            QLabel#label{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 16px;
            }}
        """)
