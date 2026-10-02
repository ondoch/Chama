from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Employee
from .serializers import EmployeeSerializer, SelfProfileSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('user').all().order_by('-id')
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        if status_param is not None:
            is_active = status_param.lower() in ['true', '1']
            queryset = queryset.filter(status=is_active)
        return queryset

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        try:
            employee = request.user.employee
        except Employee.DoesNotExist:
            return Response({"detail": "Employee profile not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = self.get_serializer(employee)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = SelfProfileSerializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        