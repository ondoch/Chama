from rest_framework import serializers

from chama.serializers import employee_code

from .models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(source="employee.pk", read_only=True)
    employee_number = serializers.SerializerMethodField()
    employee_name = serializers.CharField(source="employee.user.get_full_name", read_only=True)
    assigned_by = serializers.CharField(source="assigned_by.email", read_only=True, default=None)

    class Meta:
        model = Assignment
        fields = ["id", "chama", "employee_id", "employee_number", "employee_name", "assigned_by",
                  "assigned_at", "unassigned_at"]
        read_only_fields = fields

    def get_employee_number(self, assignment):
        return employee_code(assignment.employee)
    