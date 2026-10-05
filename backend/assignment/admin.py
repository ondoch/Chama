from django.contrib import admin
from django.contrib import admin

from .models import Assignment

# Register your models here.

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("chama", "employee", "assigned_at", "unassigned_at")
