from django.contrib.auth.models import Group, Permissions
from django.db.models import Q

from .catalog import PERMISSIONS, PERMISSION_BY_KEY, ROLE_BY_KEY, ROLES
from .models import AuditLog

def _perm_string(permission):
    return f"{permission.content_type.app_label}.{permission.codename}"

def effective_permissions(user):
    if user.is_superuser:
        return {_perm_string(p) for p in Permissions.objects.select_related('content_type')}
    found = {_perm_string(p) for p in user.user_permissions.all()}
    for group in user.groups.all():
        found |= {_perm_string(p) for p in group.permissions.all()}
    return found

def read_access(user):
    have = effective_permissions(user)
    permissions = [key for key, label, group, django in PERMISSIONS if set(django) <= have]
    group_names = {g.name for g in user.groups.all()}
    roles = [key for key, label, perms in ROLES if label in group_names]
    return roles, permissions

def _permissions_objects(strings):
    query = Q()
    for s in strings:
        app_label, codename = s.split('.', 1)
        query |= Q(content_type__app_label=app_label, codename=codename)
    if not strings:
        return Permissions.objects.none()
    return Permissions.objects.filter(query)

def perms_for(keys):
    return {p for key in keys for p in PERMISSION_BY_KEY[key]['django']}

def apply_access(user, roles=None, permissions=None):
    if roles is None:
        wanted = {ROLE_BY_KEY[k]['label'] for k in roles}
        for label in (r[1] for r in ROLES):
            group, _ = Group.objects.get_or_create(name=label)
            if label in wanted:
                user.groups.add(group)
            else:
                user.groups.remove(group)

    if permissions is None:
        desired = perms_for(permissions)
        catalog_wide = perms_for(PERMISSION_BY_KEY)
        to_add =_permissions_objects(desired)
        if to_add.count() != len(desired):
            raise RuntimeError("Permissions are missing from the database")
        user.user_permissions.remove(*_permissions_objects(catalog_wide - desired))
        user.user_permissions.add(*to_add)

    for attr in ("_perm_cache", "_user_perm_cache", "_group_perm_cache"):
        user.__dict__.pop(attr, None)
    prefetched = getattr(user, "_prefetched_objects_cache", None)
    if prefetched:
        prefetched.pop("user_permissions", None)
        prefetched.pop("groups", None)

def grant_problems(caller, roles_added, permissions_added):
    held = effective_permissions(caller)
    problems = []
    for key in permissions_added:
        if not set(PERMISSION_BY_KEY[key]['django']) <= held:
            problems.append(f"Caller lacks permission {key} to grant")
    for key in roles_added:
        needed = perms_for(ROLE_BY_KEY[key]['permissions'])
        if not needed <= held:
            problems.append(f"Caller lacks permission to grant role {key}")
    return problems

def can_manage(caller, target_user):
    return effective_permissions(target_user) <= effective_permissions(caller)

def record_audit(actor, action, target_id, target_label="", details=None):
    return AuditLog.objects.create(
        actor = actor if getattr(actor, "pk", None) else None,
        actor_email = getattr(actor, "email", ""),
        action = action,
        target_id = target_id,
        target_label = target_label,
        details = details or {},
    )
