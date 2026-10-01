from django.contrib import admin
from .models import AuditLog

# Register your models here.
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["id", "actor_email", "action", "target_id", "target_label", "created_at"]
    list_filter = ["action", "created_at"]
    search_fields = ["actor_email", "target_id"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
