import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from .usermanager import UserManager

class User(AbstractUser):
    username = None

    public_id = models.UUIDField(
        db_index=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    email = models.EmailField(
        db_index=True,
        unique=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
        