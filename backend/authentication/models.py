import uuid
from django.db import models
from .usermanager import UserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = None
    public_id = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    first_name = models.CharField(
        max_length=True
    )
    last_name = models.CharField(
        max_length=True
    )
    email = models.EmailField(
        db_index=True,
        unique=True
    )
    phone_number = models.CharField(
        max_length=15
    )
    national_ID = models.CharField(
        max_length=15
    )
    employee_ID = models.CharField(
        max_length=15
    )
    job_title = models.CharField(
        max_length=255
    )
    employement_date = models.CharField(
        max_length=15
    )
    status = models.BooleanField(
        default=False
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
