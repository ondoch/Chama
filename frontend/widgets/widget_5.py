from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt

from components.banner import Banner
from components.search_input import SearchInput
from components.form_dropdown import FormDropdown
from components.custom_table import CustomTable
from components.status_badge import StatusBadge
from components.style_constants import COLOR_BORDER, FONT_FAMILY, COLOR_TEXT_MUTED


class Widget5(QFrame):

    ROLE_OPTIONS = ["Member", "Treasurer", "Chair", "Secretary"]

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        container = QWidget()
        container.setObjectName("container")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0,0,0,0)

        banner = Banner(
            "resources/chama.svg",
            "Chama Assignements",
            "Assign employee to specific chamas.",
        )

        search_container = QWidget()
        search_container_layout = QHBoxLayout(search_container)

        search_input = SearchInput("Search...")
        drop_down = FormDropdown(
            "Select a chama...",
            ["Mwangaza Women Chama", "Tumaini Group", "Upendo Chama"],
            height=40,
            icon_path="resources/down_arrow.svg",
        )

        search_container_layout.addWidget(search_input, alignment=Qt.AlignLeft)
        search_container_layout.addWidget(drop_down, alignment=Qt.AlignRight)

        header_1 = QLabel("Available Chamas")
        header_1.setObjectName("header_1")

        table_1 = CustomTable([
            {"header": "", "type": "checkbox", "key": "selected", "width": 40},
            {"header": "Chama Name", "type": "text", "key": "name"},
            {"header": "Members", "type": "text", "key": "members", "center": True},
            {
                "header": "Status",
                "key": "status",
                "factory": lambda value, row: StatusBadge(value),
            },
        ])
        table_1.populate([
            {"name": "Mwangaza Women Chama", "members": 32, "status": "Active"},
            {"name": "Tumaini Group", "members": 18, "status": "Onboarding"},
            {"name": "Upendo Chama", "members": 5, "status": "Active"},
        ])

        header_2 = QLabel("Role in Chamas")
        header_2.setObjectName("header_2")

        sub_header = QLabel("Define what this employee will do in each assigned chama")
        sub_header.setObjectName("sub_header")

        table_2 = CustomTable([
            {"header": "Chama Name", "type": "text", "key": "name"},
            {
                "header": "Role in chama",
                "key": "role",
                "factory": self._make_role_dropdown,
            },
            {
                "header": "Actions",
                "type": "actions",
                "actions": [
                    ("Edit", self.edit_member),
                    ("Remove", self.remove_member),
                ],
            },
        ])
        table_2.populate([
            {"name": "Mwangaza Women Chama", "role": "Treasurer"},
            {"name": "Tumaini Group", "role": "Member"},
            {"name": "Upendo Chama", "role": "Member"},
        ])

        container_layout.addWidget(banner, alignment=Qt.AlignLeft)
        container_layout.addWidget(search_container)
        container_layout.addWidget(header_1)
        container_layout.addWidget(table_1)
        container_layout.addWidget(header_2)
        container_layout.addWidget(sub_header)
        container_layout.addWidget(table_2)
        main_layout.addWidget(container)

        self.setLayout(main_layout)

  
    def _make_role_dropdown(self, value, row):
        dropdown = FormDropdown(placeholder="Select role", items=self.ROLE_OPTIONS, height=30)
        if value:
            index = dropdown.findText(value)
            if index >= 0:
                dropdown.setCurrentIndex(index)
        return dropdown

    def edit_member(self, row):
        print("edit", row)

    def remove_member(self, row):
        print("remove", row)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QLabel#header_1, #header_2{{
                font-family: "Segoe UI";
                font-size: 15px;
                font-weight: 600;
                margin-left: 20px;
            }}
            QLabel#sub_header{{
                font-family: '{FONT_FAMILY}';
                font-size: 13px;
                font-weight: 400;
                color: {COLOR_TEXT_MUTED};
                background-color: transparent;
                margin-left: 20px;
            }}
        """)