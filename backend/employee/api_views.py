from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from access.services import record_audit

from .models import Employee
from .permissions import EmployeePermission
from .serializers import EmployeeSerializer, SelfProfileSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = (
        Employee.objects.select_related("user")
        .prefetch_related(
            "user__groups",
            "user__groups__permissions__content_type",
            "user__user_permissions__content_type",
        )
        .order_by("-id")
    )
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, EmployeePermission]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Assumes Employee.status is a BooleanField.
        status_param = self.request.query_params.get("status")
        if status_param:
            value = status_param.lower()
            if value in ("active", "true", "1"):
                queryset = queryset.filter(status=True)
            elif value in ("inactive", "false", "0"):
                queryset = queryset.filter(status=False)

        return queryset

    def perform_destroy(self, instance):
        if instance.user_id == self.request.user.pk:
            raise PermissionDenied("You cannot delete your own account.")

        record_audit(
            actor=self.request.user,
            action="delete_employee",
            target_id=instance.id,
            target_label=str(instance),
            details={"email": instance.user.email},
        )
        instance.user.delete()  # cascades to Employee if the OneToOne is CASCADE

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        try:
            employee = request.user.employee
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Employee profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.method == "GET":
            serializer = self.get_serializer(employee)
            return Response(serializer.data)

        serializer = SelfProfileSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    