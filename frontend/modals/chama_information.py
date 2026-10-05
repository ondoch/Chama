from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QMessageBox
)
from widgets.chama_widget import AddChama


def _set_field(field, value):
    value = "" if value is None else str(value)
    for name in ("setValue", "setText", "setCurrentText"):
        if hasattr(field, name):
            getattr(field, name)(value)
            return
    inner = getattr(field, "entry", None)
    if inner is not None and hasattr(inner, "setText"):
        inner.setText(value)


class ChamaInformation(QDialog):
    def __init__(self, parent=None, chama=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Chama" if chama else "Add Chama")
        self.setModal(True)

        self.values = {}

        layout = QVBoxLayout(self)
        self.chama_info = AddChama()
        layout.addWidget(self.chama_info)
        self.chama_info.cancel_clicked.connect(self.reject)

        self.chama_info.tab_1.next_clicked.connect(self.saveValues)

        if chama:
            self.prefill(chama)

    def prefill(self, chama):
        tab_1 = self.chama_info.tab_1
        _set_field(tab_1.chama_name, chama.get("chama_name"))
        _set_field(tab_1.description, chama.get("description"))
        _set_field(tab_1.contribution, chama.get("contribution"))
        _set_field(tab_1.pool_percentage, chama.get("pool_percentage"))
        _set_field(tab_1.registration_number, chama.get("registration_number"))
        _set_field(tab_1.meeting_frequency, chama.get("meeting_frequency"))
        _set_field(tab_1.share_percentage, chama.get("share_percentage"))
        _set_field(tab_1.loan_percentage, chama.get("loan_percentage"))

    def saveValues(self):
        tab_1 = self.chama_info.tab_1

        fields = {
            "Chama Name": tab_1.chama_name,
            "Description": tab_1.description,
            "Contribution": tab_1.contribution,
            "Pool Percentage": tab_1.pool_percentage,
            "Registration Number": tab_1.registration_number,
            "Meeting Frequency": tab_1.meeting_frequency,
            "Share Percentage": tab_1.share_percentage,
            "Loan Percentage": tab_1.loan_percentage,
        }

        empty_fields = []
        for label, field in fields.items():
            is_empty = field.isEmpty()
            field.setError(is_empty)
            if is_empty:
                empty_fields.append(label)

        if empty_fields:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please fill in the following field(s):\n- " + "\n- ".join(empty_fields)
            )
            return

        self.values = {
            "chama_name": tab_1.chama_name.returnValue(),
            "description": tab_1.description.returnValue(),
            "contribution": tab_1.contribution.returnValue(),
            "pool_percentage": tab_1.pool_percentage.returnValue(),
            "registration_number": tab_1.registration_number.returnValue(),
            "meeting_frequency": tab_1.meeting_frequency.returnValue(),
            "share_percentage": tab_1.share_percentage.returnValue(),
            "loan_percentage": tab_1.loan_percentage.returnValue(),
        }
        self.accept()
