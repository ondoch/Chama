from PyQt5.QtWidgets import QDialog, QVBoxLayout, QMessageBox
from tabs.chama.tab_2 import Tab2

class MemberInformation(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Member")
        self.setModal(True)

        self.values = {}

        layout = QVBoxLayout(self)
        self.member_info = Tab2()
        layout.addWidget(self.member_info)

        self.member_info.widget_1.next_btn.clicked.connect(self.savePersonalInfo)
        self.member_info.widget_2.next_btn.clicked.connect(self.saveResidentialInfo)
        self.member_info.widget_3.next_btn.clicked.connect(self.saveEmploymentInfo)
        self.member_info.widget_4.next_btn.clicked.connect(self.saveNextOfKinInfo)
        self.member_info.finished.connect(self.saveValues)

    def _validateFields(self, fields):
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
        return empty_fields

    def savePersonalInfo(self):
        w = self.member_info.widget_1

        fields = {
            "Full name": w.full_name,
            "Date of birth": w.date_picker,
            "Phone number": w.phone_number,
            "Email address": w.email_address,
            "Nationality": w.nationality,
            "National ID": w.national_id,
            "PIN": w.pin,
        }

        if self._validateFields(fields):
            return

        self.values["Personal details"] = {
            "full name": w.full_name.returnValue(),
            "date of birth": w.date_picker.returnValue(),
            "phone number": w.phone_number.returnValue(),
            "email address": w.email_address.returnValue(),
            "gender": w.radio.get_gender(),
            "marital status": w.radio.get_marital_status(),
            "nationality": w.nationality.returnValue(),
            "national ID": w.national_id.returnValue(),
            "pin": w.pin.returnValue(),
        }

        self.member_info.residentialInfo()

    def saveResidentialInfo(self):
        w = self.member_info.widget_2

        fields = {
            "Country of residence": w.country,
            "County of residence": w.county,
            "Town/city of residence": w.town,
            "Estate": w.estate,
            "Physical address": w.physical_address,
            "Postal address": w.postal_address,
            "Postal code": w.postal_code,
        }

        if self._validateFields(fields):
            return

        self.values["Residential information"] = {
            "country of residence": w.country.returnValue(),
            "county of residence": w.county.returnValue(),
            "town/city of residence": w.town.returnValue(),
            "estate": w.estate.returnValue(),
            "physical address": w.physical_address.returnValue(),
            "postal address": w.postal_address.returnValue(),
            "postal code": w.postal_code.returnValue(),
        }

        self.member_info.employmentInfo()

    def saveEmploymentInfo(self):
        w = self.member_info.widget_3

        fields = {
            "Employment status": w.employment_status,
            "Employer/business name": w.employer,
            "Occupation/job title": w.occupation,
            "Employer/business address": w.business_address,
            "Source of income": w.source_of_income,
        }

        if self._validateFields(fields):
            return

        self.values["Employment information"] = {
            "employment status": w.employment_status.returnValue(),
            "employment/Business name": w.employer.returnValue(),
            "occupation/job title": w.occupation.returnValue(),
            "employer/business address": w.business_address.returnValue(),
            "source of income": w.source_of_income.returnValue(),
        }

        self.member_info.nextOfKin()

    def saveNextOfKinInfo(self):
        w = self.member_info.widget_4

        fields = {
            "Full name": w.full_name,
            "Relationship": w.relationship,
            "Phone number": w.phone_number,
            "Physical address": w.address,
        }

        if self._validateFields(fields):
            return

        self.values["Next of kin information"] = {
            "full name": w.full_name.returnValue(),
            "relationship": w.relationship.returnValue(),
            "phone number": w.phone_number.returnValue(),
            "physical address": w.address.returnValue(),
        }

        self.member_info.uploads()

    def saveUploads(self):
        self.values["Uploads"] = {
        }
        print(self.values)

    def saveValues(self):
        print(self.values)
        self.accept()