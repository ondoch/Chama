from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from .models import Chama
from .services import ChamaClosed


INFO_FIELDS = {
    "chama_name",
    "description",
    "registration_number",
}

SETTINGS_FIELDS = {
    "meeting_frequency",
    "contribution",
    "share_percentage",
    "pool_percentage",
    "loan_percentage",
}


def employee_brief(employee):
    if employee is None:
        return None

    return {
        "id": employee.pk,
        "employee_ID": employee.employee_ID,
        "name": employee.user.get_full_name(),
    }


def open_assignments(chama):
    return list(
        chama.assignments
        .filter(unassigned_at__isnull=True)
        .select_related("employee__user")
    )


class ChamaSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    officials_count = serializers.SerializerMethodField()
    assigned_to = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Chama

        fields = [
            "public_id",
            "chama_name",
            "registration_number",
            "description",
            "meeting_frequency",
            "contribution",
            "share_percentage",
            "pool_percentage",
            "loan_percentage",
            "status",
            "created_at",
            "created_by",
            "member_count",
            "officials_count",
            "assigned_to",
        ]

        read_only_fields = [
            "public_id",
            "status",
            "created_at",
            "created_by",
            "member_count",
            "officials_count",
            "assigned_to",
        ]

    def get_member_count(self, chama):
        count = getattr(chama, "member_count", None)

        if count is not None:
            return count

        return chama.members.filter(is_active=True).count()

    def get_officials_count(self, chama):
        count = getattr(chama, "officials_count", None)

        if count is not None:
            return count

        return chama.officials.filter(ended_on__isnull=True).count()

    def get_assigned_to(self, chama):
        return [
            employee_brief(assignment.employee)
            for assignment in open_assignments(chama)
        ]

    def get_created_by(self, chama):
        return employee_brief(chama.created_by)

    def validate_registration_number(self, value):
        value = value.strip()

        if not value:
            return ""

        qs = Chama.objects.filter(
            registration_number__iexact=value
        )

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "A chama with this registration number already exists."
            )

        return value

    def validate(self, attrs):
        # Creating a new chama
        if self.instance is None:
            return attrs

        # Closed chamas cannot be edited
        if self.instance.status == Chama.Status.CLOSED:
            raise ChamaClosed()

        user = self.context["request"].user

        changed = {
            field
            for field, value in attrs.items()
            if getattr(self.instance, field) != value
        }

        # Updating chama information
        if changed & INFO_FIELDS:
            if not user.has_perm("access.update_chama_info"):
                raise PermissionDenied(
                    "You don't have authority to perform such actions"
                )

        # Updating chama settings
        if changed & SETTINGS_FIELDS:
            if not user.has_perm("access.configure_chama_settings"):
                raise PermissionDenied(
                    "You don't have authority to perform such actions"
                )

        return attrs
    