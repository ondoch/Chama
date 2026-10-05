import datetime
from django.db import models
from django.db import models
from django.db.models import Q

# Create your models here.
class ChamaMember(models.Model):
    chama = models.ForeignKey("chama.Chama", on_delete=models.CASCADE, related_name="members")
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=16)
    national_id = models.CharField(max_length=8, blank=True)
    email = models.EmailField(blank=True)
    joined_on = models.DateField(default=datetime.date.today)
    is_active = models.BooleanField(default=True)
    removed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["full_name"]
        constraints = [
            models.UniqueConstraint(fields=["chama", "national_id"],
                                    condition=Q(is_active=True) & ~Q(national_id=""),
                                    name="uniq_active_member_national_id"),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.chama})"
