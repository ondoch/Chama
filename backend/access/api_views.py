from rest_framework import filters, viewsets
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
            "roles": [{"key": key, "label": label, "permissions": perms} for key, label, perms in ROLES],
            "permissions": [{"key": key, "label": label, "group": group} for key, label, group, _django in PERMISSIONS],
        })

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [PasswordUpToDate, has_perm("access.view_auditlog")]
    filter_backends = [filters.SearchFilter]
    search_fields = ["actor_email", "action", "target_id"]

    def get_queryset(self):
        qs = AuditLog.objects.all()
        action = self.request.query_params.get("action")
        return qs.filter(action=action) if action else qs
