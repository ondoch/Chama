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
