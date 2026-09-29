from django.contrib import admin
from .models import User
from .form import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "email",
    )
    list_filter = (
        "is_active", "is_staff", "is_superuser"
    )
    fieldsets = (
        (None, {"fields":("email","password")}),
        ("Permissions", {"fields":("is_staff","is_superuser","groups","user_permissions")}),
        ("Important dates", {"fields":("last_login","date_joined")})
    )
    add_fieldsets = (
        (
            None, {
                "classes":("wide",),
                "fields":(
                    "email","password1","password2"
                )
            }
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(User, UserAdmin)
