from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

from components.custom_table import CustomTable
from components.style_constants import FONT_FAMILY, COLOR_TEXT_PRIMARY


def build_columns(on_view=None):
    def view_clicked(row, btn=None):
        if on_view:
            on_view(row)
        else:
            print("View", row)

    return [
        {"header": "Date", "key": "date"},
        {"header": "Members", "key": "members", "center": True},
        {"header": "Amount", "key": "amount", "center": True}
    ]


GROUP_COLUMNS = build_columns()

SAMPLE_DATA = [
    {"date": "Sep 1, 2025", "members": "Mary Wanjiku", "amount": "KES 12,000"},
    {"date": "Auf 25, 2025", "members": "Mary Wanjiku", "amount": "KES 12,000"},
    {"date": "Aug 18, 2025", "members": "Mary Wanjiku", "amount": "KES 12,000"},
    {"date": "Aug 11, 2025", "members": "Mary Wanjiku", "amount": "KES 12,000"},
]


class RecentContributionTable(CustomTable):
    def __init__(self, on_view=None):
        super().__init__(build_columns(on_view))

    def load_sample_data(self):
        self.populate(SAMPLE_DATA)

