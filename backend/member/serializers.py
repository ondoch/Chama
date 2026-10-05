from rest_framework import serializers

from chama.models import Chama
from chama.services import ChamaClosed

from .models import ChamaMember


class MemberSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()
    joined_on = serializers.DateField(input_formats=["iso-8601", "%d/%m/%Y"], required=False)

    class Meta:
        model = ChamaMember
        fields = ["id", "chama", "full_name", "phone", "national_id", "email", "role", "role_display",
                  "joined_on", "is_active", "removed_at"]
        read_only_fields = ["id", "chama", "is_active", "removed_at"]

    @staticmethod
    def _office(member):
        return next((o for o in member.offices.all() if o.ended_on is None), None)

    def get_role(self, member):
        office = self._office(member)
        return office.position if office else "member"

    def get_role_display(self, member):
        office = self._office(member)
        return office.get_position_display() if office else "Member"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context["request"].user
        if not (user.has_perm("access.update_member_information") or user.has_perm("access.add_members")):
            data.pop("national_id", None)
        return data

    def validate(self, attrs):
        chama = self.context["chama"]
        if chama.status == Chama.Status.CLOSED:
            raise ChamaClosed()
        if self.instance is not None and not self.instance.is_active:
            raise serializers.ValidationError("This member has been removed and can no longer be changed.")

        others = chama.members.filter(is_active=True)
        if self.instance is not None:
            others = others.exclude(pk=self.instance.pk)
        national_id = attrs.get("national_id")
        if national_id and others.filter(national_id=national_id).exists():
            raise serializers.ValidationError({"national_id": "This person is already a member of this chama."})
        sent_role = str(getattr(self, "initial_data", {}).get("role", "member") or "member").strip().lower()
        if sent_role != "member":
            raise serializers.ValidationError({"role": (
                f"Offices are appointed separately: POST /api/chamas/{chama.pk}/officials/ "
                f'with {{"member": <id>, "position": "{sent_role}"}}.')})
        return attrs
