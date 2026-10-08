from django.db.models import Count, Q
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from access.permissions import has_perm
from access.services import record_audit
from authentication.permissions import PasswordUpToDate
from employee.models import Employee

from .models import Chama
from .permissions import ChamaPermission
from .serializers import ChamaSerializer, employee_code
from .services import (
    ALLOWED_TRANSITIONS,
    ChamaClosed,
    has_oversight,
    only_unassigned,
    scoped_chamas,
    with_extras,
)

TRUE = ("1", "true", "True")


def employee_of(user):
    return getattr(user, "employee", None)


class ChamaViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ChamaSerializer
    permission_classes = [PasswordUpToDate, ChamaPermission]
    lookup_field = "public_id"
    filter_backends = [filters.SearchFilter]
    search_fields = ["chama_name", "registration_number", "description"]

    def get_queryset(self):
        qs = (
            with_extras(scoped_chamas(self.request.user))
            .select_related("created_by__user")
            .prefetch_related("assignments__employee__user")
        )
        params = self.request.query_params

        if params.get("status"):
            qs = qs.filter(status=params["status"])

        # Chamas nobody currently owns (no open assignment)
        if params.get("unassigned") in TRUE:
            qs = only_unassigned(qs)

        # Chamas a given employee currently has. A subquery is used (instead of
        # joining assignments onto qs) so the annotated member/official counts
        # from with_extras are not multiplied by the join.
        assigned_to = params.get("assigned_to")
        if assigned_to:
            if not assigned_to.isdigit():
                raise ValidationError({"assigned_to": "Must be an employee id."})
            mine = Chama.objects.filter(
                assignments__employee_id=int(assigned_to),
                assignments__unassigned_at__isnull=True,
            ).values("pk")
            qs = qs.filter(pk__in=mine)

        return qs

    def fresh(self, chama):
        return self.get_serializer(
            with_extras(Chama.objects.filter(pk=chama.pk)).get()
        ).data

    def perform_create(self, serializer):
        me = employee_of(self.request.user)
        chama = serializer.save(created_by=me)
        record_audit(
            self.request.user,
            "chama.created",
            chama.pk,
            chama.chama_name,
            {
                "registration_number": chama.registration_number,
                "created_by": employee_code(me),
            },
        )

    def perform_update(self, serializer):
        fields = (
            "chama_name",
            "registration_number",
            "description",
            "meeting_frequency",
            "contribution",
            "share_percentage",
            "pool_percentage",
            "loan_percentage",
        )
        before = {f: str(getattr(serializer.instance, f)) for f in fields}
        chama = serializer.save()
        changes = {
            f: [before[f], str(getattr(chama, f))]
            for f in fields
            if before[f] != str(getattr(chama, f))
        }
        if changes:
            record_audit(self.request.user, "chama.updated", chama.pk, chama.chama_name, changes)

    @action(detail=True, methods=["post"], url_path="set-status")
    def set_status(self, request, *args, **kwargs):
        chama = self.get_object()
        if chama.status == Chama.Status.CLOSED:
            raise ChamaClosed()
        new = str(request.data.get("status", "")).strip().lower()
        if new not in Chama.Status.values:
            raise ValidationError(
                {"status": f"Choose one of: {', '.join(Chama.Status.values)}."}
            )
        if new not in ALLOWED_TRANSITIONS[chama.status]:
            raise ValidationError(
                {"status": f"A {chama.status} chama cannot become {new}."}
            )
        old, chama.status = chama.status, new
        chama.save(update_fields=["status", "updated_at"])
        record_audit(
            request.user,
            "chama.status_changed",
            chama.pk,
            chama.chama_name,
            {"from": old, "to": new, "reason": str(request.data.get("reason", ""))[:300]},
        )
        return Response(self.fresh(chama))

    @action(detail=False, methods=["get"])
    def stats(self, request):
        visible = scoped_chamas(request.user)
        data = {
            "total": visible.count(),
            **{value: visible.filter(status=value).count() for value in Chama.Status.values},
            "members": visible.aggregate(
                n=Count("members", filter=Q(members__is_active=True))
            )["n"],
        }
        if has_oversight(request.user):
            data["unassigned"] = only_unassigned(visible).count()
        return Response(data)


class ChamaReportView(APIView):
    permission_classes = [PasswordUpToDate, has_perm("access.view_reports")]

    def get(self, request):
        workload = (
            Employee.objects.filter(
                assignments__isnull=False, assignments__unassigned_at__isnull=True
            )
            .annotate(
                n_chamas=Count(
                    "assignments",
                    filter=Q(assignments__unassigned_at__isnull=True),
                    distinct=True,
                ),
                n_members=Count(
                    "assignments__chama__members",
                    distinct=True,
                    filter=Q(
                        assignments__unassigned_at__isnull=True,
                        assignments__chama__members__is_active=True,
                    ),
                ),
            )
            .select_related("user")
            .order_by("-n_chamas", "user__first_name")
        )
        return Response(
            {
                "total_chamas": Chama.objects.count(),
                "chamas_by_status": {
                    v: Chama.objects.filter(status=v).count() for v in Chama.Status.values
                },
                "unassigned_chamas": only_unassigned(Chama.objects.all()).count(),
                "active_members": Chama.objects.aggregate(
                    n=Count("members", filter=Q(members__is_active=True))
                )["n"],
                "workload": [
                    {
                        "employee_id": e.pk,
                        "employee_number": employee_code(e),
                        "name": e.user.get_full_name(),
                        "chamas": e.n_chamas,
                        "active_members": e.n_members,
                    }
                    for e in workload
                ],
            }
        )