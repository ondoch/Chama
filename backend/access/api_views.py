from django.utils.dateparse import parse_date
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissions import PasswordUpToDate

from .catalog import PERMISSIONS, ROLES
from .models import AuditLog
from .permissions import has_perm
from .serializers import AuditLogSerializer


class CatalogView(APIView):
    permission_classes = [IsAuthenticated, PasswordUpToDate]

    def get(self, request):
        return Response({
            "roles": [
                {"key": key, "label": label, "permissions": perms}
                for key, label, perms in ROLES
            ],
            "permissions": [
                {"key": key, "label": label, "group": group}
                for key, label, group, _django in PERMISSIONS
            ],
        })


class AuditLogPagination(PageNumberPagination):
    page_size = 10                       # default when the client sends no page_size
    page_size_query_param = "page_size"
    max_page_size = 100                  # keep in sync with MAX_PAGE_SIZE in the dashboard


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    pagination_class = AuditLogPagination
    permission_classes = [PasswordUpToDate, has_perm("access.view_audits")]
    filter_backends = [filters.SearchFilter]
    search_fields = ["actor_email", "action", "target_id", "target_label"]

    def get_queryset(self):
        qs = AuditLog.objects.all().order_by("-created_at", "-id")
        params = self.request.query_params

        if params.get("action"):
            qs = qs.filter(action=params["action"])

        date_from = parse_date(params.get("date_from") or "")
        date_to = parse_date(params.get("date_to") or "")
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        return qs
    