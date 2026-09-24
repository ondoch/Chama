from PyQt5.QtWidgets import (
    QVBoxLayout,
    QMessageBox,
    QDialog
)
from widgets.employee_widget import AddEmployee

class EmployeeInformation(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Employee")
        self.setModal(True)

        self.values = {}
        self.employee_data = {}

        layout = QVBoxLayout(self)
        self.add_employee = AddEmployee()
        layout.addWidget(self.add_employee)

        self.add_employee.tab_1.employee_info.next_button.clicked.connect(self.savePersonalInfo)
        self.add_employee.tab_2.next_btn.clicked.connect(self.saveRolesandPermissions)
        self.add_employee.tab_3.finish_btn.clicked.connect(self.saveValues)

    def _validate(self, fields):
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
        employee_info = self.add_employee.tab_1.employee_info

        fields = {
            "first name": employee_info.first_name,
            "email address": employee_info.email_address,
            "national ID": employee_info.national_id,
            "job title": employee_info.job_title,
            "last name": employee_info.last_name,
            "phone number": employee_info.phone_number,
            "employee ID": employee_info.employee_id,
            "employment date": employee_info.employment_date,
        }

        if self._validate(fields):
            return

        self.values["Personal Information"] = {
            "first name": employee_info.first_name.returnValue(),
            "email address": employee_info.email_address.returnValue(),
            "national id": employee_info.national_id.returnValue(),
            "job title": employee_info.job_title.returnValue(),
            "last name": employee_info.last_name.returnValue(),
            "phone number": employee_info.phone_number.returnValue(),
            "employee ID": employee_info.employee_id.returnValue(),
            "employment date": employee_info.employment_date.returnValue(),
            "status": "Active" if employee_info.toggle.isChecked() else "Inactive",
        }

        self.add_employee.employeeInformation()

    def saveRolesandPermissions(self):
        permissions_info_1 = self.add_employee.tab_2.widget_1
        permissions_info_2 = self.add_employee.tab_2.widget_2

        self.values["Roles and Permissions"] = {
            "Roles & Permissions": {
                "Chama facilitator": permissions_info_1.check_1.returnValue(),
                "Chama supervisor": permissions_info_1.check_2.returnValue(),
                "Finance support": permissions_info_1.check_3.returnValue(),
                "Super admin": permissions_info_1.check_4.returnValue(),
            },
            "Chama management": {
                "Create chama": permissions_info_2.chama_management.create_chama.returnValue(),
                "View chama details": permissions_info_2.chama_management.view_chama.returnValue(),
                "Update chama info": permissions_info_2.chama_management.update_chama.returnValue(),
                "Configure chama settings": permissions_info_2.chama_management.chama_settings.returnValue(),
            },
            "Member management": {
                "Add members": permissions_info_2.member_management.add_members.returnValue(),
                "View members": permissions_info_2.member_management.view_members.returnValue(),
                "Update member information": permissions_info_2.member_management.update_members.returnValue(),
                "Remove member": permissions_info_2.member_management.remove_members.returnValue(),
            },
            "System access": {
                "View reports": permissions_info_2.system_access.view_reports.returnValue(),
                "View audits": permissions_info_2.system_access.view_audits.returnValue(),
                "Manage employees": permissions_info_2.system_access.manage_employees.returnValue(),
            },
        }

    def saveValues(self):
        personal = self.values.get("Personal Information", {})
        first_name = personal.get("first name", "")
        last_name = personal.get("last name", "")
        job_title = personal.get("job title", "")
        status = personal.get("status", "Inactive")

        self.employee_data = {
            "name": f"{first_name} {last_name}".strip(),
            "role": job_title,
            "chamas_managed": str(self.add_employee.tab_3.widget_1.getChamaCount()),
            "status": status,
        }

        print(self.values)
        self.accept()
