from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt

from components.style_constants import (
    FONT_FAMILY,
    COLOR_TEXT_PRIMARY,
)
from components.custom_table import CustomTable
from components.search_input import SearchInput

ROLE_STYLES = {
    "chairperson": {"bg": "#cfe8ff", "text": "#1c5d99", "border": "#8fc4f0"},
    "treasurer":   {"bg": "#d7f7df", "text": "#1e7a4c", "border": "#8fdba8"},
    "secretary":   {"bg": "#fff6b8", "text": "#8a6d00", "border": "#e6d27a"},
    "member":      {"bg": "#e6f4ff", "text": "#1c5d99", "border": None},
}

OFFICIAL_ROLES = {"chairperson", "treasurer", "secretary"}

def _make_role_badge(role_value, row_data):
    role_key = (role_value or "member").strip().lower()
    style = ROLE_STYLES.get(role_key, ROLE_STYLES["member"])

    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignCenter)

    label = QLabel(role_value or "Member")
    label.setAlignment(Qt.AlignCenter)

    if role_key in OFFICIAL_ROLES and style["border"]:
        border_css = f"border: 1px solid {style['border']};"
    else:
        border_css = "border: none;"

    label.setStyleSheet(f"""
        QLabel {{
            background-color: {style['bg']};
            color: {style['text']};
            {border_css}
            border-radius: 4px;
            padding: 4px 14px;
            font-family: '{FONT_FAMILY}';
            font-size: 12px;
            font-weight: 600;
        }}
    """)

    layout.addWidget(label)
    return container


class MemberSummary(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        header = QLabel("Mwangaza Women Group")
        header.setObjectName("header")

        search = SearchInput("Search member...")

        columns = [
            {"header": "Name", "key": "name"},
            {
                "header": "Role",
                "key": "role",
                "factory": _make_role_badge,
                "width": 160,
            },
        ]
        self.table = CustomTable(columns)

        main_layout.addWidget(header)
        main_layout.addWidget(search, alignment=Qt.AlignLeft)
        main_layout.addWidget(self.table)

    def setStylesheet(self):
        self.setStyleSheet(f"""
            QLabel#header {{
                font-family: '{FONT_FAMILY}';
                font-size: 14px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
                background-color: transparent;
            }}
        """)

    def set_members(self, members: list):
        self.table.populate(members)
