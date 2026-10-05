import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Chama(models.Model):
    class Status(models.TextChoices):
        ONBOARDING = "onboarding", "Onboarding"
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"
        CLOSED = "closed", "Closed"

    public_id = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    chama_name = models.CharField(
        max_length=255
    )

    registration_number = models.CharField(
        max_length=255,
        unique=True
    )

    description = models.TextField()

    meeting_frequency = models.CharField(
        max_length=255
    )

    contribution = models.IntegerField(
        default=0
    )

    share_percentage = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    pool_percentage = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    loan_percentage = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.ONBOARDING)
    created_by = models.ForeignKey("employee.Employee", null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="created_chamas")

    def __str__(self):
        return self.chama_name
