from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout
)
from components.form_dropdown import FormDropdown
from components.custom_table import CustomTable

class MembersTable(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)

        drop_down = FormDropdown(
            "Select a chama...",
            ["Mwangaza Women Chama", "Tumaini Group", "Upendo Chama"],
            height=40,
            icon_path="resources/down_arrow.svg",
        )

        columns = [
            {"header": "Member Name", "key": "name"},
            {"header": "Phone Number", "key": "phone", "center": True},
            {"header": "Member Since", "key": "member_since", "center": True},
        ]

        table = CustomTable(columns)
        main_layout.addWidget(table)

        members = [
            {"name": "Wanjiku Mwangi", "phone": "0712 345 678", "member_since": "Jan 2023"},
            {"name": "Otieno Odhiambo", "phone": "0723 456 789", "member_since": "Mar 2023"},
            {"name": "Amina Hassan", "phone": "0734 567 890", "member_since": "Jun 2024"},
        ]

        table.populate(members)
