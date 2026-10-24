from components.custom_table import CustomTable
from components.status_badge import StatusBadge



def make_status_cell(value, row_data):
    return StatusBadge(value or "inactive")


def build_columns(on_view=None):
    def view_clicked(row, btn=None):
        if on_view:
            on_view(row)
        else:
            print("View", row)

    return [
        {"header": "Date", "key": "date"},
        {"header": "Member", "key": "member", "center": True},
        {"header": "Amount", "key": "amount", "center": True},
        {"header": "Status", "key": "status", "factory": make_status_cell},
    ]


GROUP_COLUMNS = build_columns()

SAMPLE_DATA = [
    {"date": "Sep 5, 2025", "member": "Peter Mwangi", "amount": "KES 80,000", "status": "Active"},
    {"date": "Aug 23, 2025", "member": "Susan Wanjiku", "amount": "KES 15,000", "status": "Active"},
    {"date": "Aug 12, 2025", "member": "James Karanja", "amount": "KES 20,000", "status": "Inactive"},
]


class RecentLoansTable(CustomTable):
    def __init__(self, on_view=None):
        super().__init__(build_columns(on_view))

    def load_sample_data(self):
        self.populate(SAMPLE_DATA)
