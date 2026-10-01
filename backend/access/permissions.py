from rest_framework.permissions import BasePermission

def has_perm(perm):
    class HasPerm(BasePermission):
        def has_permission(self, request, view):
            return bool(request.user and request.user.is_authenticated and request.user.has_perm(perm))

    HasPerm.__name__ = f"HasPerm_{perm.replace('.', '_')}"
    return HasPerm
