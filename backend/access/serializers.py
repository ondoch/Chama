from rest_framework import serializers

from .models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ["id", "actor_email", "action", "target_id", "target_label", "details", "created_at"]
        read_only_fields = fields
