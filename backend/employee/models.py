from django.db import models
from django.conf import settings

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee"
    )
    phone_number = models.CharField(
        max_length=15
    )
    national_ID = models.CharField(
        unique=True,
        max_length=20
    )
    employee_ID = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        editable=False
    )
    job_title = models.CharField(
        max_length=255
    )
    employment_date = models.DateField()
    status = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.job_title}"

    def save(self, *args, **kwargs):
        if not self.employee_ID:
            last_employee = (
                Employee.objects
                .exclude(employee_ID__isnull=True)
                .exclude(employee_ID="")
                .order_by("-id")
                .first()
            )

            if last_employee:
                try:
                    last_id = int(last_employee.employee_ID.split("-")[-1])
                except (ValueError, AttributeError):
                    last_id = 0
            else:
                last_id = 0

            self.employee_ID = f"EMP-{last_id + 1:04d}"

        super().save(*args, **kwargs)
