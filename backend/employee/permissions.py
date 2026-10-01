from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from access.services import can_manage

class EmployeePermission(BasePermission):
    action_permissions = {
        "list": "employee.view_employee",
        "create": "employee.add_employee",
        "update": "employee.change_employee",
        "partial_update": "employee.change_employee",
        "destroy": "employee.delete_employee",
        "reset_password": "employee.change_employee",
        "stats": "employee.view_employee",
    }

    guarded_actions = {"update", "partial_update", "destroy", "reset_password"}

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        perm = self.action_perms.get(view.action)
        return request.user.has_perm(perm) if perm else True

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            return obj.user_id == request.user.id or request.user.has_perm("employee.view_employee")
        if view.action in self.guarded_actions and not can_manage(request.user, obj.user):
            raise PermissionDenied("You cannot change someone who has more access than you.")
        return True
