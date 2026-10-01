from rest_framework.permissions import BasePermission

class PasswordUpToDate(BasePermission):
    message = "You must change your password before proceeding."
    def has_permissions(self, request, user):
        user = request.user
        return not(user and user.is_authenticated and user.must_change_password)
