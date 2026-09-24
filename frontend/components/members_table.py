from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

from components.custom_table import CustomTable
from components.avatar import Avatar
from components.status_badge import StatusBadge
from components.action_buttons import ActionButtonGroup
from components.style_constants import FONT_FAMILY, COLOR_TEXT_PRIMARY

def make_avatar_cell(value, row_data):
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(8, 0, 0, 0)
    layout.setSpacing(8)
    layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

    layout.addWidget(Avatar(text=value))

    name_label = QLabel(value or "")
    name_label.setStyleSheet(
        f"font-family: {FONT_FAMILY}; color: {COLOR_TEXT_PRIMARY}; font-size: 14px;"
    )
    layout.addWidget(name_label)
    layout.addStretch()
    return container

def make_status_cell(value, row_data):
    return StatusBadge(value or "inactive")

def actions_factory(actions_config):
    def factory(value, row_data):
        return ActionButtonGroup(actions_config, row_data=row_data)
    return factory

GROUP_COLUMNS = [
    {"header": "Employee", "key": "name", "factory": make_avatar_cell},
    {"header": "Role", "key": "role"},
    {"header": "Chamas Managed", "key": "chamas_managed"},
    {"header": "Status", "key": "status", "factory": make_status_cell},
    {"header": "Actions", "key": None, "width": 110,
     "factory": actions_factory([
         {"label": "View", "width": 60, "callback": lambda row, btn: print("View", row)},
     ])},
]


class MembersTable(CustomTable):
    def __init__(self):
        super().__init__(GROUP_COLUMNS)
