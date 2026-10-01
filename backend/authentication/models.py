import uuid
from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = None

    public_id = models.UUIDField(
        db_index=True,
        editable=False,
        default=uuid.uuid4,
        unique=True
    )
    email = models.EmailField(
        unique=True,
        db_index=True
    )
    must_change_password = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
