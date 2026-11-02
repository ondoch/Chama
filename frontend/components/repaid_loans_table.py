from components.custom_table import CustomTable

def build_columns(on_view=None):
    def view_clicked(row, btn=None):
        if on_view:
            on_view(row)
        else:
            print("View", row)

    return [
        {"header": "Member", "key": "member", "center":True},
        {"header": "Amount Requested", "key": "amount_requested", "center":True},
        {"header": "Date Requested", "key": "date_requested", "center":True},
        {"header": "Date Cleared", "key": "date_cleared", "center":True},
    ]

GROUP_COLUMNS = build_columns()


class RepaidLoansTable(CustomTable):
    def __init__(self, on_view=None):
        super().__init__(build_columns(on_view))

