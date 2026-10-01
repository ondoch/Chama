from django.db import models
from django.conf import settings

# Create your models here.
class AccessControl(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = [
            ("create_chama", "Create chama"),
            ("view_chama_details", "View chama details"),
            ("update_chama_info", "Update chama info"),
            ("configure_chama_settings", "Configure chama settings"),
            ("add_members", "Add members"),
            ("view_members", "View members"),
            ("update_member_information", "Update member information"),
            ("remove_member", "Remove member"),
            ("view_reports", "View reports"),
            ("view_audits", "View audits"),
        ]

class AuditLog(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    actor_email = models.CharField(max_length=254)
    action = models.CharField(max_length=100)
    target_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    target_label = models.CharField(
        max_length=100,
        blank=True
    )
    details = models.JSONField(
        default=dict,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AuditLog: {self.action} by {self.actor_email} on {self.created_at:%Y-%m-%d %H:%M:%S}"
