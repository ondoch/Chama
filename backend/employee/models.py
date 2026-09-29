from django.conf import settings
from django.db import models


class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee",
    )
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    phone_number = models.CharField(
        max_length=20
    )
    national_ID = models.CharField(
        max_length=20,
        unique=True
    )
    employee_ID = models.CharField(
        max_length=20,
        unique=True
    )
    job_title = models.CharField(
        max_length=100
    )
    employment_date = models.CharField()
    status = models.BooleanField(
        default=False
    )

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
