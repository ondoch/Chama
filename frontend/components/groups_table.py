from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

from components.custom_table import CustomTable
from components.avatar import Avatar
from components.action_buttons import ActionButtonGroup
from components.style_constants import FONT_FAMILY, COLOR_TEXT_PRIMARY


def _make_avatar_cell(value, row_data):
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


def _actions_factory(actions_config):
    def factory(value, row_data):
        return ActionButtonGroup(actions_config, row_data=row_data)
    return factory


GROUP_COLUMNS = [
    {"header": "Group name", "key": "name", "factory": _make_avatar_cell},
    {"header": "Members", "key": "member_count"},
    {"header": "Contribution", "key": "contribution"},
    {"header": "Created on", "key": "created_on"},
    {"header": "Actions", "key": None, "width": 110,
     "factory": _actions_factory([
         {"label": "View", "width": 60, "callback": lambda row: print("View", row)},
         {"icon": "resources/more-vertical.svg", "callback": lambda row: print("More", row)},
     ])},
]


class GroupsTable(CustomTable):
    def __init__(self):
        super().__init__(GROUP_COLUMNS)