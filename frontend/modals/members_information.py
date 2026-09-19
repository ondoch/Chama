from PyQt5.QtWidgets import QDialog, QVBoxLayout
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

    def savePersonalInfo(self):
        self.values["Personal details"] = {
            "full name": self.member_info.widget_1.full_name.returnValue(),
            "date of birth": self.member_info.widget_1.date_picker.returnValue(),
            "phone number": self.member_info.widget_1.phone_number.returnValue(),
            "email address": self.member_info.widget_1.email_address.returnValue(),
            "gender": self.member_info.widget_1.radio.get_gender(),
            "marital status": self.member_info.widget_1.radio.get_marital_status(),
            "nationality": self.member_info.widget_1.nationality.returnValue(),
            "national ID": self.member_info.widget_1.national_id.returnValue(),
            "pin": self.member_info.widget_1.pin.returnValue(),
        }

    def saveResidentialInfo(self):
        self.values["Residential information"] = {
            "country of residence":self.member_info.widget_2.country.returnValue(),
            "county of residence":self.member_info.widget_2.county.returnValue(),
            "town/city of residence":self.member_info.widget_2.town.returnValue(),
            "estate":self.member_info.widget_2.estate.returnValue(),
            "physical address":self.member_info.widget_2.physical_address.returnValue(),
            "postal address":self.member_info.widget_2.postal_address.returnValue(),
            "postal code":self.member_info.widget_2.postal_code.returnValue(),
        }

    def saveEmploymentInfo(self):
        self.values["Employment information"] = {
            "employment status":self.member_info.widget_3.employment_status.returnValue(),
            "employment/Business name":self.member_info.widget_3.employer.returnValue(),
            "occupation/job title":self.member_info.widget_3.occupation.returnValue(),
            "employer/business address":self.member_info.widget_3.business_address.returnValue(),
            "source of income":self.member_info.widget_3.source_of_income.returnValue(),
        }

    def saveNextOfKinInfo(self):
        self.values["Next of kin information"] = {
            "full name":self.member_info.widget_4.full_name.returnValue(),
            "relationship":self.member_info.widget_4.relationship.returnValue(),
            "phone number":self.member_info.widget_4.phone_number.returnValue(),
            "physical address":self.member_info.widget_4.address.returnValue(),
        }

    def saveUploads(self):
        self.values["Uploads"] = {
        }
        print(self.values)

    def saveValues(self):
        print(self.values)
        self.accept()
