from django.db import models
from django.conf import settings
from django.db.models import Q

# Create your models here.
class Assignment(models.Model):
    chama = models.ForeignKey("chama.Chama", on_delete=models.CASCADE, related_name="assignments")
    employee = models.ForeignKey("employee.employee", on_delete=models.CASCADE, related_name="assignments")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    assigned_at = models.DateTimeField(auto_now_add=True)
    unassigned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['assigned_at']
        constraints = [
            models.UniqueConstraint(fields=["chama", "employee"], condition=Q(unassigned_at__isnull=True),
                                    name="uniq_active_assignment"),
        ]

    def __str__(self):
        return f"{self.employee} -> {self.chama}"
