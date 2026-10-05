from rest_framework.permissions import BasePermission

class ChamaPermission(BasePermission):
    action_perms = {
        "list":["access.view_chama_details"],
        "retrieve":["access.view_chama_details"],
        "stats":["access.view_chama_details"],
        "create":["access.create_chama"],
        "update":["access.update_chama_info", "access.configure_chama_settings"],
        "partial_update":["access.update_chama_info", "access.configure_chama_settings"],
        "set_status":["accesss.configure_chama_settings"],
    }

    def has_permissions(self, request, view):
        if not(request.user and request.user.is_authenticated):
            return False
        if view.action == "metadata":
            return True
        return any(request.user.has_perm(p) for p in self.action_perms.get(view.action, []))
