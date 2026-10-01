from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import Employee
from .serializers import EmployeeSerializer
from .permissions import EmployeePermission

class EmployeeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [EmployeePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['employee_ID', 'user__email', 'user__first_name', 'user__last_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(user=user)
        return queryset

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        total_employees = Employee.objects.count()
        active_employees = Employee.objects.filter(status='active').count()
        inactive_employees = Employee.objects.filter(status='inactive').count()

        data = {
            'total_employees': total_employees,
            'active_employees': active_employees,
            'inactive_employees': inactive_employees,
        }
        return Response(data, status=status.HTTP_200_OK)
