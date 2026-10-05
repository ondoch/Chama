from django.contrib import admin

from .models import ChamaMember


@admin.register(ChamaMember)
class ChamaMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "chama", "phone", "is_active")
    list_filter = ("is_active",)
    search_fields = ("full_name", "chama__name")
