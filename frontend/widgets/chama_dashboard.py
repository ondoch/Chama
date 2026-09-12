from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QWidget,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtCore import Qt

from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER
)
from components.search_input import SearchInput
from components.form_dropdown import FormDropdown
from components.groups_table import GroupsTable
from components.pagination import Pagination

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
        header_widget_layout = QVBoxLayout(header_widget)

        header = QLabel("Groups")
        header.setObjectName("header")
        label = QLabel("View and manage all groups")
        label.setObjectName("label")
        search_widget = QWidget()
        search_widget_layout = QHBoxLayout(search_widget)
        search = SearchInput("Search...")
        dropdown = FormDropdown(
            "Select a chama...",
            ["Mwangaza Women Chama", "Tumaini Group", "Upendo Chama"],
            height=40,
            icon_path="resources/down_arrow.svg",
        )

        search_widget_layout.addWidget(search, alignment=Qt.AlignLeft)
        search_widget_layout.addWidget(dropdown, alignment=Qt.AlignRight)

        container_widget_layout.addWidget(header_widget)
        container_widget_layout.addWidget(header)
        container_widget_layout.addWidget(label)
        container_widget_layout.addWidget(search_widget)

        self.table = GroupsTable()
        self.table.populate([
            {"name": "Group name", "member_count": "8 members",
             "contribution": "KSh 2,500", "created_on": "May 10, 2024"},
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
        """)