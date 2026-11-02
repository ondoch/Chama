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
        {"header": "Member", "key": "member", "center":True},
        {"header": "Amount Requested", "key": "amount_requested", "center":True},
        {"header": "Purpose", "key": "purpose", "center":True},
        {"header": "Date Requested", "key": "date_requested", "center":True},
        {"header": "Status", "key": "status", "factory": make_status_cell},
    ]

GROUP_COLUMNS = build_columns()


class AllLoansTable(CustomTable):
    def __init__(self, on_view=None):
        super().__init__(build_columns(on_view))
