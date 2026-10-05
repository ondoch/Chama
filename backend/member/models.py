import datetime

from django.db import models
from django.db.models import Q


class ChamaMember(models.Model):
    chama = models.ForeignKey("chama.Chama", on_delete=models.CASCADE, related_name="members")

    # --- Personal details ---
    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=16)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=20, blank=True)
    marital_status = models.CharField(max_length=20, blank=True)
    nationality = models.CharField(max_length=60, blank=True)
    national_id = models.CharField(max_length=8, blank=True)
    kra_pin = models.CharField(max_length=20, blank=True)

    # --- Residential information ---
    country = models.CharField(max_length=60, blank=True)
    county = models.CharField(max_length=60, blank=True)
    town = models.CharField(max_length=80, blank=True)
    estate = models.CharField(max_length=100, blank=True)
    physical_address = models.CharField(max_length=255, blank=True)
    postal_address = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    # --- Employment information ---
    employment_status = models.CharField(max_length=50, blank=True)
    employer_name = models.CharField(max_length=150, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    employer_address = models.CharField(max_length=255, blank=True)
    source_of_income = models.CharField(max_length=100, blank=True)

    # --- Next of kin ---
    kin_full_name = models.CharField(max_length=150, blank=True)
    kin_relationship = models.CharField(max_length=50, blank=True)
    kin_phone = models.CharField(max_length=16, blank=True)
    kin_address = models.CharField(max_length=255, blank=True)

    # --- Membership ---
    joined_on = models.DateField(default=datetime.date.today)
    is_active = models.BooleanField(default=True)
    removed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["full_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["chama", "national_id"],
                condition=Q(is_active=True) & ~Q(national_id=""),
                name="uniq_active_member_national_id",
            ),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.chama})"
