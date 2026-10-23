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


def build_columns(on_view=None):
    def view_clicked(row, btn=None):
        if on_view:
            on_view(row)
        else:
            print("View", row)

    return [
        {"header": "Chama name", "key": "chama_name", "factory": make_avatar_cell},
        {"header": "Members", "key": "members", "center": True},
        {"header": "Total contributions", "key": "total_contributions", "center": True},
        {"header": "Total loans", "key": "total_loans", "center": True},
        {"header": "Status", "key": "status", "factory": make_status_cell},
        {"header": "Actions", "key": None, "width": 110,
         "factory": actions_factory([
             {"label": "View Report", "width": 80, "callback": view_clicked},
         ])},
    ]


GROUP_COLUMNS = build_columns()

SAMPLE_DATA = [
    {"chama_name": "Umoja Savers", "members": 24,
     "total_contributions": "KES 480,000", "total_loans": "KES 210,000", "status": "active"},
    {"chama_name": "Jitegemee Group", "members": 18,
     "total_contributions": "KES 360,000", "total_loans": "KES 150,000", "status": "active"},
    {"chama_name": "Tujenge Welfare", "members": 12,
     "total_contributions": "KES 96,000", "total_loans": "KES 40,000", "status": "onboarding"},
    {"chama_name": "Mwangaza Investors", "members": 30,
     "total_contributions": "KES 750,000", "total_loans": "KES 320,000", "status": "active"},
    {"chama_name": "Harambee Women", "members": 15,
     "total_contributions": "KES 225,000", "total_loans": "KES 90,000", "status": "inactive"},
    {"chama_name": "Pamoja Youth", "members": 20,
     "total_contributions": "KES 140,000", "total_loans": "KES 55,000", "status": "onboarding"},
    {"chama_name": "Nyota Traders", "members": 27,
     "total_contributions": "KES 540,000", "total_loans": "KES 260,000", "status": "active"},
    {"chama_name": "Bidii Farmers", "members": 16,
     "total_contributions": "KES 192,000", "total_loans": "KES 70,000", "status": "inactive"},
]


class ReportsTable(CustomTable):
    def __init__(self, on_view=None):
        super().__init__(build_columns(on_view))

    def load_sample_data(self):
        self.populate(SAMPLE_DATA)
