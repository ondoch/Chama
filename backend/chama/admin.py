from django.contrib import admin

from .models import Chama


@admin.register(Chama)
class ChamaAdmin(admin.ModelAdmin):
    list_display = ("chama_name", "registration_number","status")
    list_filter = ("status",)
    search_fields = ("chama_name", "registration_number")