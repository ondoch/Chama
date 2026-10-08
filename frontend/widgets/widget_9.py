from datetime import datetime
from PyQt5.QtWidgets import QFrame, QHBoxLayout
from components.custom_table import CustomTable


def _fmt_date(value):
    if not value:
        return "—"
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).strftime("%b %Y")
    except ValueError:
        return str(value)


def normalize_member(m):
    return {
        "id": m.get("id"),
        "name": m.get("full_name") or "Unknown",
        "phone": m.get("phone") or "—",
        "member_since": _fmt_date(m.get("joined_on")),
    }


class MembersTable(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)
        columns = [
            {"header": "Member Name", "key": "name"},
            {"header": "Phone Number", "key": "phone", "center": True},
            {"header": "Member Since", "key": "member_since", "center": True},
        ]
        self.table = CustomTable(columns)
        main_layout.addWidget(self.table)

    def set_members(self, members):
        self.table.populate(members)
