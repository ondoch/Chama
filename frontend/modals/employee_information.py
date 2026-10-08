from datetime import date

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QMessageBox,
    QDialog
)

from api.api_client import CreateEmployeeWorker, UpdateEmployeeWorker
from widgets.employee_widget import AddEmployee


def _slug(label):
    return label.strip().lower().replace(" & ", "_and_").replace(" ", "_")


def _is_active(status):
    if status is None:
        return True
    if isinstance(status, str):
        return status.strip().lower() == "active"
    return bool(status)


class EmployeeInformation(QDialog):
    def __init__(self, api_client, employee=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.employee = employee or {}
        self.employee_id = self.employee.get("id")
        self.is_edit = self.employee_id is not None

        self.setWindowTitle("Edit Employee" if self.is_edit else "Add Employee")
        self.setModal(True)

        self.values = {}
        self.created_employee = {}
        self.save_worker = None

        layout = QVBoxLayout(self)
        self.add_employee = AddEmployee(api_client)
        layout.addWidget(self.add_employee)

        self.add_employee.tab_1.employee_info.next_button.clicked.connect(self.savePersonalInfo)
        self.add_employee.tab_2.next_btn.clicked.connect(self.saveRolesandPermissions)
        self.add_employee.tab_3.finish_btn.clicked.connect(self.saveValues)

        self._prefill()

    def _permission_fields(self):
        p1 = self.add_employee.tab_2.widget_1
        p2 = self.add_employee.tab_2.widget_2
        return {
            "Roles & Permissions": {
                "Chama facilitator": p1.check_1,
                "Chama supervisor": p1.check_2,
                "Finance support": p1.check_3,
                "Super admin": p1.check_4,
            },
            "Chama management": {
                "Create chama": p2.chama_management.create_chama,
                "View chama details": p2.chama_management.view_chama,
                "Update chama info": p2.chama_management.update_chama,
                "Configure chama settings": p2.chama_management.chama_settings,
            },
            "Member management": {
                "Add members": p2.member_management.add_members,
                "View members": p2.member_management.view_members,
                "Update member information": p2.member_management.update_members,
                "Remove member": p2.member_management.remove_members,
            },
            "System access": {
                "View reports": p2.system_access.view_reports,
                "View audits": p2.system_access.view_audits,
                "Manage employees": p2.system_access.manage_employees,
            },
        }

    def _prefill(self):
        emp = self.employee
        info = self.add_employee.tab_1.employee_info

        first = emp.get("first_name") or ""
        last = emp.get("last_name") or ""
        if not (first or last) and emp.get("name"):
            first, _, last = str(emp["name"]).partition(" ")

        info.first_name.setValue(first)
        info.last_name.setValue(last)
        info.email_address.setValue(emp.get("email", ""))
        info.phone_number.setValue(emp.get("phone_number") or emp.get("phone") or "")
        info.national_id.setValue(emp.get("national_ID", ""))
        info.job_title.setValue(emp.get("job_title", ""))
        default_date = "" if self.is_edit else date.today().isoformat()
        info.employment_date.setValue(emp.get("employment_date") or default_date)
        info.toggle.setChecked(_is_active(emp.get("status")), animate=False)

        roles = set(emp.get("roles") or [])
        perms = set(emp.get("permissions") or [])
        for group, boxes in self._permission_fields().items():
            wanted = roles if group == "Roles & Permissions" else perms
            for label, box in boxes.items():
                box.setValue(_slug(label) in wanted)

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
        self.values["Roles and Permissions"] = {
            group: {label: box.returnValue() for label, box in boxes.items()}
            for group, boxes in self._permission_fields().items()
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

        if self.is_edit:
            self.save_worker = UpdateEmployeeWorker(self.api_client, self.employee_id, payload)
        else:
            self.save_worker = CreateEmployeeWorker(self.api_client, payload)
        self.save_worker.success.connect(self._on_saved)
        self.save_worker.error.connect(self._on_save_error)
        self.save_worker.start()

    def _on_saved(self, result):
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
        elif self.is_edit:
            QMessageBox.information(self, "Employee updated", "The changes were saved.")

        self.accept()

    def _on_save_error(self, message):
        self.add_employee.tab_3.finish_btn.setEnabled(True)
        title = "Could not update employee" if self.is_edit else "Could not create employee"
        QMessageBox.critical(self, title, message)

    def reject(self):
        if self.save_worker is not None and self.save_worker.isRunning():
            return
        super().reject()
