from django.apps import apps
from django.db.models import Count, Exists, OuterRef, Prefetch, Q
from rest_framework.exceptions import APIException

from .models import Chama


ASSIGN_PERM = "access.assign_chamas"


ALLOWED_TRANSITIONS = {
    Chama.Status.ONBOARDING: {
        Chama.Status.ACTIVE,
        Chama.Status.CLOSED,
    },
    Chama.Status.ACTIVE: {
        Chama.Status.SUSPENDED,
        Chama.Status.CLOSED,
    },
    Chama.Status.SUSPENDED: {
        Chama.Status.ACTIVE,
        Chama.Status.CLOSED,
    },
    Chama.Status.CLOSED: set(),
}


class ChamaClosed(APIException):
    status_code = 400
    default_detail = "This chama is closed and can no longer be changed"
    default_code = "chama_closed"


def has_oversight(user):
    return bool(
        user.is_superuser
        or user.has_perm(ASSIGN_PERM)
        or user.has_perm("access.view_all_chamas")
    )


def scoped_chamas(user):
    chamas = Chama.objects.all()

    if has_oversight(user):
        return chamas

    employee = getattr(user, "employee", None)

    if employee is None or employee.status == "terminated":
        return chamas.none()

    return chamas.filter(
        assignments__employee=employee,
        assignments__unassigned_at__isnull=True,
    )


def only_unassigned(chamas):
    Assignment = apps.get_model("assignment", "Assignment")

    return chamas.filter(
        ~Exists(
            Assignment.objects.filter(
                chama=OuterRef("pk"),
                unassigned_at__isnull=False,
            )
        )
    )


def with_extras(queryset):
    Assignment = apps.get_model("assignment", "Assignment")

    return queryset.annotate(
        member_count=Count(
            "members",
            filter=Q(members__is_active=True),
            distinct=True,
        )
    ).prefetch_related(
        Prefetch(
            "assignments",
            queryset=Assignment.objects.filter(
                unassigned_at__isnull=True
            ).select_related(
                "employee__user"
            ),
            to_attr="open_assignments",
        )
    )
