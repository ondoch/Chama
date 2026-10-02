from django.contrib.auth.models import Group, Permission
from django.db.models import Q

from .catalog import (
    PERMISSIONS,
    PERMISSION_BY_KEY,
    ROLE_BY_KEY,
    ROLES,
)
from .models import AuditLog


def _perm_string(permission):
    return (
        f"{permission.content_type.app_label}."
        f"{permission.codename}"
    )


def effective_permissions(user):
    if user.is_superuser:
        return {
            _perm_string(permission)
            for permission in Permission.objects.select_related(
                "content_type"
            )
        }

    found = {
        _perm_string(permission)
        for permission in user.user_permissions.all()
    }

    for group in user.groups.all():
        found |= {
            _perm_string(permission)
            for permission in group.permissions.all()
        }

    return found


def read_access(user):
    have = effective_permissions(user)

    permissions = [
        key
        for key, label, group, django in PERMISSIONS
        if set(django) <= have
    ]

    group_names = {
        group.name
        for group in user.groups.all()
    }

    roles = [
        key
        for key, label, perms in ROLES
        if label in group_names
    ]

    return roles, permissions


def _permissions_objects(strings):
    query = Q()

    for permission_string in strings:

        app_label, codename = permission_string.split(".", 1)

        query |= Q(
            content_type__app_label=app_label,
            codename=codename
        )

    if not strings:
        return Permission.objects.none()

    return Permission.objects.filter(query)


def perms_for(keys):
    return {
        permission
        for key in keys
        for permission in PERMISSION_BY_KEY[key]["django"]
    }


def apply_access(user, roles=None, permissions=None):
    if roles is not None:

        wanted_roles = {
            ROLE_BY_KEY[key]["label"]
            for key in roles
        }

        existing_groups = {
            group.name: group
            for group in Group.objects.all()
        }

        managed_role_names = {
            label
            for key, label, perms in ROLES
        }

        user.groups.remove(
            *Group.objects.filter(
                name__in=managed_role_names
            )
        )

        for role_name in wanted_roles:

            group = existing_groups.get(role_name)

            if group is None:
                group = Group.objects.create(
                    name=role_name
                )

            user.groups.add(group)

    if permissions is not None:

        desired = perms_for(permissions)

        catalog_wide = perms_for(
            PERMISSION_BY_KEY
        )

        user.user_permissions.remove(
            *_permissions_objects(
                catalog_wide - desired
            )
        )
        user.user_permissions.add(
            *_permissions_objects(desired)
        )


def grant_problems(
    caller,
    roles_added,
    permissions_added
):
    held = effective_permissions(caller)

    problems = []

    for key in permissions_added:

        if not set(
            PERMISSION_BY_KEY[key]["django"]
        ) <= held:

            problems.append(
                f"Caller lacks permission {key} to grant"
            )

    for key in roles_added:

        needed = perms_for(
            ROLE_BY_KEY[key]["permissions"]
        )

        if not needed <= held:

            problems.append(
                f"Caller lacks permission to grant role {key}"
            )

    return problems


def can_manage(caller, target_user):
    return (
        effective_permissions(target_user)
        <= effective_permissions(caller)
    )


def record_audit(
    actor,
    action,
    target_id=None,
    target_label="",
    details=None
):
    return AuditLog.objects.create(
        actor=(
            actor
            if getattr(actor, "pk", None)
            else None
        ),

        actor_email=getattr(
            actor,
            "email",
            ""
        ),

        action=action,

        target_id=target_id,

        target_label=target_label,

        details=details or {},
    )
