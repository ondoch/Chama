from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QMessageBox,
    QDialog
)

from api.api_client import CreateEmployeeWorker
from widgets.employee_widget import AddEmployee

def _slug(label):
    return label.strip().lower().replace(" & ", "_and_").replace(" ", "_")

class EmployeeInformation(QDialog):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("Add Employee")
        self.setModal(True)

        self.values = {}
        self.created_employee = {}
        self.create_worker = None

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

    def _status_value(self, label):
        return label == "Active"

    def _build_payload(self):
        personal = self.values.get("Personal Information", {})
        rp = self.values.get("Roles and Permissions", {})

        roles = [
            _slug(label)
            for label, enabled in rp.get("Roles & Permissions", {}).items()
            if enabled
        ]

        permissions = [
            _slug(label)
            for group, items in rp.items()
            if group != "Roles & Permissions"
            for label, enabled in items.items()
            if enabled
        ]

        return {
            "first_name": personal.get("first name", ""),
            "last_name": personal.get("last name", ""),
            "email": personal.get("email address", ""),
            "phone_number": personal.get("phone number", ""),
            "national_ID": personal.get("national id", ""),
            "job_title": personal.get("job title", ""),
            "employment_date": personal.get("employment date", ""),
            "status": self._status_value(personal.get("status", "Active")),
            "roles": roles,
            "permissions": permissions,
        }

    def saveValues(self):
        if "Personal Information" not in self.values:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please complete the personal information step first."
            )
            return

        self.saveRolesandPermissions()
        payload = self._build_payload()

        self.add_employee.tab_3.finish_btn.setEnabled(False)

        self.create_worker = CreateEmployeeWorker(self.api_client, payload)
        self.create_worker.success.connect(self._on_created)
        self.create_worker.error.connect(self._on_create_error)
        self.create_worker.start()

    def _on_created(self, result):
        self.created_employee = result

        temp_password = result.get("temporary_password")
        if temp_password:
            box = QMessageBox(self)
            box.setIcon(QMessageBox.Information)
            box.setWindowTitle("Employee Created")
            box.setText(
                f"Temporary password:\n\n{temp_password}\n\n"
                "Copy it now. It will not be shown again."
            )
            box.setTextInteractionFlags(Qt.TextSelectableByMouse)
            box.exec()

        self.accept()

    def _on_create_error(self, message):
        self.add_employee.tab_3.finish_btn.setEnabled(True)
        QMessageBox.critical(self, "Could not create employee", message)

    def reject(self):
        if self.create_worker is not None and self.create_worker.isRunning():
            return
        super().reject()
