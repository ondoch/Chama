from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout
)

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from components.banner_4 import Banner4
from components.form_dropdown import FormDropdown
from components.members_table import MembersTable
from components.search_input import SearchInput
from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER,
)

class Onboarding(QFrame):
    def __init__(self):
        super().__init__()

        self.initUi()
        self.setStylesheet()

    def initUi(self):
        main_layout = QVBoxLayout(self)

        container_widget = QWidget()
        container_widget.setObjectName("container_widget")
        container_widget_layout = QVBoxLayout(container_widget)

        header_widget = QWidget()
        header_widget_layout = QHBoxLayout(header_widget)
        header_widget_layout.setContentsMargins(20, 0, 0, 0)

        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(10, 0, 0, 0)
        header_widget_layout.setSpacing(0)

        icon = QLabel()
        icon.setFixedSize(50, 50)
        pixmap = QPixmap("resources/onboarding_1.svg")
        icon.setPixmap(
            pixmap.scaled(49, 49, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        header = QLabel("Onboarding")
        header.setObjectName("header")
        label = QLabel("Track chama setup and identify incomplete onboarding.")
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

        carrier_widget = QWidget()
        carrier_widget_layout = QHBoxLayout(carrier_widget)

        table_layout = QVBoxLayout()

        search_widget = QWidget()
        search_widget_layout = QHBoxLayout(search_widget)

        self.search = SearchInput("Search...")

        drop_down_widget = QWidget()
        drop_down_widget_layout = QHBoxLayout(drop_down_widget)

        facilitator = QLabel("Facilitator")
        facilitator.setObjectName("header_1")
        progress = QLabel("Progress")
        progress.setObjectName("header_1")
        status = QLabel("Status")
        status.setObjectName("header_1")

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

        drop_down_widget_layout.addWidget(facilitator)
        drop_down_widget_layout.addWidget(self.facilitators_dropdown)
        drop_down_widget_layout.addWidget(progress)
        drop_down_widget_layout.addWidget(self.progress_dropdown)
        drop_down_widget_layout.addWidget(status)
        drop_down_widget_layout.addWidget(self.status_dropdown)

        search_widget_layout.addWidget(self.search, alignment=Qt.AlignLeft)
        search_widget_layout.addWidget(drop_down_widget, alignment=Qt.AlignRight)
        

        table_layout.addWidget(search_widget)

        carrier_widget_layout.addLayout(table_layout)
        carrier_widget_layout.setContentsMargins(0,0,0,0)

        container_widget_layout.addWidget(top_row_widget)
        container_widget_layout.addLayout(banner_layout)
        container_widget_layout.addWidget(carrier_widget)

        main_layout.addWidget(container_widget)

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
            QLabel#header_1{{
                font-family: {FONT_FAMILY};
                color:{COLOR_TEXT_MUTED};
                font-size: 16px;
            }}
        """)
