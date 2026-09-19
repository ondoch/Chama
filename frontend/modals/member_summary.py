from PyQt5.QtWidgets import QDialog, QVBoxLayout

from widgets.widget_12 import MemberSummary as MemberSummaryWidget

# Trial data — stand-in until group members come from the database.
TRIAL_MEMBERS = [
    {"name": "Mary Wanjiku", "role": "Chairperson"},
    {"name": "Peter Otieno", "role": "Treasurer"},
    {"name": "Jane Njeri", "role": "Secretary"},
    {"name": "John Kamau", "role": "Member"},
]


class MemberSummaryDialog(QDialog):
    def __init__(self, parent=None, members=None):
        super().__init__(parent)
        self.setWindowTitle("Member Summary")
        self.resize(420, 320)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.summary = MemberSummaryWidget()
        layout.addWidget(self.summary)

        # Once groups carry a real "members" list, pass it in via the
        # `members` kwarg (see GroupsTable.openMemberSummaryDialog) and
        # this trial fallback stops being used.
        self.summary.set_members(members if members is not None else TRIAL_MEMBERS)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = MemberSummaryDialog()
    dialog.show()
    sys.exit(app.exec_())