from .models import User
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)

class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ("email",)
        