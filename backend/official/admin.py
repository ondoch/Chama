from django.contrib import admin

from .models import Official


@admin.register(Official)
class OfficialAdmin(admin.ModelAdmin):
    list_display = ("chama", "position", "member", "appointed_on", "ended_on")
    list_filter = ("position",)
    search_fields = ("chama__name", "member__full_name")
