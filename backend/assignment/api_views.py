from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from access.permissions import has_perm
from access.services import record_audit
from authentication.permissions import PasswordUpToDate
from chama.models import Chama
from chama.serializers import ChamaSerializer
from chama.services import ChamaClosed, scoped_chamas, with_extras
from employee.models import Employee

from .models import Assignment
from .serializers import AssignmentSerializer

class ChamaAssignmentView(APIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.chama = get_object_or_404(scoped_chamas(request.user), pk=kwargs["chama_pk"])

    def chama_response(self):
        chama = with_extras(Chama.objects.filter(pk=self.chama.pk)).get()
        return Response(ChamaSerializer(chama, context={"request": self.request}).data)

    def employee(self):
        try:
            return Employee.objects.select_related("user").get(pk=self.request.data.get("employee"))
        except (Employee.DoesNotExist, ValueError, TypeError):
            raise ValidationError({"employee": "No such employee."})

    def open_assignment(self, employee):
        return Assignment.objects.filter(chama=self.chama, employee=employee, unassigned_at__isnull=True).first()

class AssignView(ChamaAssignmentView):
    permission_classes = [PasswordUpToDate, has_perm("access.assign_chamas")]

    def post(self, request, chama_pk):
        if self.chama.status == Chama.Status.CLOSED:
            raise ChamaClosed()
        employee = self.employee()
        if employee.status == Employee.Status.TERMINATED or not employee.user.is_active:
            raise ValidationError({"employee": "A terminated employee cannot be assigned chamas."})
        if not employee.user.has_perm("access.view_chama_details"):
            raise ValidationError({"employee": "That employee does not have the 'View chama details' "
                                               "permission, so cannot work on chamas."})
        if self.open_assignment(employee):
            raise ValidationError({"employee": "This employee is already assigned to the chama."})
        Assignment.objects.create(chama=self.chama, employee=employee, assigned_by=request.user)
        record_audit(request.user, "chama.assigned", self.chama.pk, self.chama.name,
                     {"employee": employee.employee_number})
        return self.chama_response()

class UnassignView(ChamaAssignmentView):
    permission_classes = [PasswordUpToDate, has_perm("access.assign_chamas")]

    def post(self, request, chama_pk):
        if self.chama.status == Chama.Status.CLOSED:
            raise ChamaClosed()
        employee = self.employee()
        assignment = self.open_assignment(employee)
        if assignment is None:
            raise ValidationError({"employee": "This employee is not assigned to the chama."})
        assignment.unassigned_at = timezone.now()
        assignment.save(update_fields=["unassigned_at"])
        record_audit(request.user, "chama.unassigned", self.chama.pk, self.chama.name,
                     {"employee": employee.employee_number})
        return self.chama_response()

class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [PasswordUpToDate, has_perm("access.view_chama_details")]
    pagination_class = None

    def get_queryset(self):
        chama = get_object_or_404(scoped_chamas(self.request.user), pk=self.kwargs["chama_pk"])
        qs = chama.assignments.select_related("employee__user", "assigned_by")
        if self.request.query_params.get("include_past") not in ("1", "true", "True"):
            qs = qs.filter(unassigned_at__isnull=True)
        return qs
