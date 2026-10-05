from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Official(models.Model):
    class Position(models.TextChoices):
        CHAIRPERSON = "chairperson", "Chairperson"
        SECRETARY = "secretary", "Secretary"
        TREASURER = "treasurer", "Treasurer"

    chama = models.ForeignKey("chama.Chama", on_delete=models.CASCADE, related_name="officials")
    member = models.ForeignKey("member.ChamaMember", on_delete=models.CASCADE, related_name="offices")
    position = models.CharField(max_length=12, choices=Position.choices)
    appointed_on = models.DateField(default=timezone.localdate)
    appointed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name="+")
    ended_on = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["position", "-appointed_on", "-id"]
        constraints = [
            # one current holder per office, and one current office per member
            models.UniqueConstraint(fields=["chama", "position"], condition=Q(ended_on__isnull=True),
                                    name="uniq_current_office_holder"),
            models.UniqueConstraint(fields=["member"], condition=Q(ended_on__isnull=True),
                                    name="uniq_one_current_office_per_member"),
        ]

    def __str__(self):
        return f"{self.get_position_display()}: {self.member.full_name} ({self.chama})"
    