from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER,
    COLOR_SIDEBAR_BG,
    COLOR_SIDEBAR_HOVER,
    COLOR_SIDEBAR_SELECT

)
from components.search_input import SearchInput
from components.form_dropdown import FormDropdown
from components.groups_table import GroupsTable
from components.pagination import Pagination
from components.banner_4 import Banner4

class ChamaDashboard(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
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
        pixmap = QPixmap("resources/group_1.svg")
        icon.setPixmap(pixmap.scaled(49,49, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        header = QLabel("Groups")
        header.setObjectName("header")
        label = QLabel("View and manage all groups")
        label.setObjectName("label")

        header_layout.addWidget(header)
        header_layout.addWidget(label)
        header_widget_layout.addWidget(icon)
        header_widget_layout.addLayout(header_layout)

        self.add_chama_button = QPushButton("+ Add Chama")
        self.add_chama_button.setObjectName("add_chama_button")
        self.add_chama_button.setCursor(Qt.PointingHandCursor)
        self.add_chama_button.setFixedHeight(38)

        top_row_widget = QWidget()
        top_row_layout = QHBoxLayout(top_row_widget)
        top_row_layout.setContentsMargins(0, 0, 0, 0)

        top_row_layout.addWidget(header_widget, alignment=Qt.AlignLeft)
        top_row_layout.addStretch()
        top_row_layout.addWidget(self.add_chama_button, alignment=Qt.AlignRight | Qt.AlignVCenter)

        banner_layout = QHBoxLayout()
        banner_layout.setSpacing(12)

        left, top, right, bottom = banner_layout.getContentsMargins()
        banner_layout.setContentsMargins(left, 10, right, bottom)

        banner_1 = Banner4("resources/chamas.svg", "12", "Total Chamas", "3 Active")
        banner_2 = Banner4("resources/people.svg", "248", "Members", "Across all")
        banner_3 = Banner4("resources/inactive_users.svg", "4", "Pending Approvals", "Waiting for confirmation")
        banner_4 = Banner4("resources/leader_1.svg", "8", "Chama Officials", "Across all chamas")

        banner_layout.addWidget(banner_1, stretch=1)
        banner_layout.addWidget(banner_2, stretch=1)
        banner_layout.addWidget(banner_3, stretch=1)
        banner_layout.addWidget(banner_4, stretch=1)

        search_widget = QWidget()
        search_widget_layout = QHBoxLayout(search_widget)
        search = SearchInput("Search...")

        search_widget_layout.addWidget(search, alignment=Qt.AlignLeft)

        container_widget_layout.addWidget(top_row_widget)
        container_widget_layout.addLayout(banner_layout)
        container_widget_layout.addWidget(search_widget)

        self.table = GroupsTable()
        self.table.populate([
            {"name": "Group name", "member_count": "8 members",
             "contribution": "KSh 2,500", "created_on": "May 10, 2024"},
             {"name": "Mwangaza Women Group", "member_count": "14 members",
             "contribution": "KSh 500", "created_on": "October 5, 2026"},
        ])
        container_widget_layout.addWidget(self.table)

        footer = Pagination()
        container_widget_layout.addWidget(footer, alignment=Qt.AlignBottom)

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
            QPushButton#add_chama_button{{
                font-family: {FONT_FAMILY};
                background-color: {COLOR_SIDEBAR_BG};
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 600;
                border: none;
                border-radius: 6px;
                padding: 0 16px;
            }}
            QPushButton#add_chama_button:hover{{
                background: {COLOR_SIDEBAR_HOVER};
            }}
            QPushButton#add_chama_button:pressed{{
                background: {COLOR_SIDEBAR_SELECT};
            }}
        """)
