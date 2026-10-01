from django.contrib import admin
from .models import Employee

@admin.register(Employee)

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "national_ID", "employee_ID", "job_title", "employment_date", "status")
    list_filter = ("status",)
    search_fields = ("employee_ID", "user__email", "user__first_name", "user__last_name")
