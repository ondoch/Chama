from django.contrib import admin

from access.services import record_audit

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "employee_ID",
        "user",
        "phone_number",
        "national_ID",
        "job_title",
        "employment_date",
        "status",
    )

    search_fields = (
        "employee_ID",
        "user__email",
        "user__first_name",
        "user__last_name",
        "phone_number",
        "national_ID",
    )

    list_filter = (
        "status",
        "job_title",
        "employment_date",
    )

    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):
        old_values = {}

        if change and obj.pk:

            try:

                old_obj = Employee.objects.get(
                    pk=obj.pk
                )

                old_values = {
                    "phone_number": old_obj.phone_number,
                    "national_ID": old_obj.national_ID,
                    "job_title": old_obj.job_title,
                    "employment_date": str(
                        old_obj.employment_date
                    ),
                    "status": old_obj.status,
                }

            except Employee.DoesNotExist:

                old_values = {}
        super().save_model(
            request,
            obj,
            form,
            change
        )
        if not change:

            record_audit(

                actor=request.user,

                action="create_employee",

                target_id=obj.id,

                target_label=str(obj),

                details={
                    "employee_ID": obj.employee_ID,
                    "email": obj.user.email,
                    "job_title": obj.job_title,
                }
            )

            return
        changes = {}

        if old_values:

            current_values = {

                "phone_number": obj.phone_number,

                "national_ID": obj.national_ID,

                "job_title": obj.job_title,

                "employment_date": str(
                    obj.employment_date
                ),

                "status": obj.status,

            }

            for field in old_values:

                old_value = old_values[field]

                new_value = current_values[field]

                if old_value != new_value:

                    changes[field] = {

                        "old": old_value,

                        "new": new_value,

                    }
        if changes:

            record_audit(

                actor=request.user,

                action="update_employee",

                target_id=obj.id,

                target_label=str(obj),

                details=changes
            )

    def delete_model(
        self,
        request,
        obj
    ):
        employee_id = obj.id
        employee_label = str(obj)

        details = {
            "employee_ID": obj.employee_ID,
            "email": obj.user.email,
            "job_title": obj.job_title,
        }
        super().delete_model(
            request,
            obj
        )
        record_audit(

            actor=request.user,

            action="delete_employee",

            target_id=employee_id,

            target_label=employee_label,

            details=details
        )
        