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
        {"header": "Date", "key": "date", "center":True},
        {"header": "Member", "key": "member", "center":True},
        {"header": "Type", "key": "type", "factory": make_status_cell},
        {"header": "Description", "key": "description"},
        {"header": "Amount", "key": "amount", "center":True},
    ]

GROUP_COLUMNS = build_columns

DUMMY_TRANSACTIONS = [
    {"date": "Oct. 02, 2026", "member": "Wanjiku Mwangi",  "type": "Contribution",       "description": "Monthly contribution",         "amount": "KES 2,000"},
    {"date": "Oct. 02, 2026", "member": "Otieno Kamau",    "type": "Contribution",       "description": "Monthly contribution",         "amount": "KES 2,000"},
    {"date": "Oct. 05, 2026", "member": "Achieng Phelix",  "type": "Loan Disbursement",  "description": "Business loan - stock purchase", "amount": "KES 15,000"},
    {"date": "Oct. 09, 2026", "member": "James Mwangi",    "type": "Loan Repayment",     "description": "Loan repayment - instalment 2", "amount": "KES 3,500"},
    {"date": "Oct. 12, 2026", "member": "Grace Nduta",     "type": "Cycle Disbursement", "description": "Merry-go-round payout - Cycle 4", "amount": "KES 24,000"},
    {"date": "Oct. 15, 2026", "member": "Njeri Wambui",    "type": "Share Disbursement", "description": "Year-end share payout",        "amount": "KES 8,200"},
    {"date": "Oct. 18, 2026", "member": "Peter Otieno",    "type": "Other",              "description": "Meeting venue fee",            "amount": "KES 500"},
    {"date": "Oct. 21, 2026", "member": "Kiprop Langat",   "type": "Contribution",       "description": "Monthly contribution",         "amount": "KES 2,000"},
    {"date": "Oct. 25, 2026", "member": "Achieng Phelix",  "type": "Loan Repayment",     "description": "Loan repayment - instalment 1", "amount": "KES 4,000"},
    {"date": "Oct. 28, 2026", "member": "Mary Akinyi",     "type": "Other",              "description": "Stationery and record books",  "amount": "KES 750"},
]

class TransactionsTable(CustomTable):
    def __init__(self, on_view=None):
        super().__init__(build_columns(on_view))
        self.populate(DUMMY_TRANSACTIONS)
