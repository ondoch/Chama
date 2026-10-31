from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

from components.custom_table import CustomTable
from components.status_badge import StatusBadge
from components.action_buttons import ActionButtonGroup

def make_status_cell(value, row_data):
    return StatusBadge(value or "inactive")


def build_columns(on_view=None):
    def view_clicked(row, btn=None):
        if on_view:
            on_view(row)
        else:
            print("View", row)

    return [
        {"header": "Name", "key": "name", "center":True},
        {"header": "Phone", "key": "phone", "center":True},
        {"header": "Joined on", "key": "joined_on", "center":True},
        {"header": "Status", "key": "status", "factory": make_status_cell},
    ]

GROUP_COLUMNS = build_columns()


class ReportsMembersTable(CustomTable):
    def __init__(self, on_view=None):
        super().__init__(build_columns(on_view))
