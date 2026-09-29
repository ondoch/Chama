import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Chama(models.Model):

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

    def __str__(self):
        return self.chama_name
        