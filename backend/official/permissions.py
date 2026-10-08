from rest_framework.permissions import BasePermission


class OfficialPermission(BasePermission):
    action_perms = {
        "list": "access.view_members",
        "retrieve": "access.view_members",
        "create": "access.update_member_information",
        "destroy": "access.update_member_information",
        "replace_all": "access.update_member_information",
    }

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if view.action == "metadata":
            return True
        perm = self.action_perms.get(view.action)
        return bool(perm) and request.user.has_perm(perm)
    