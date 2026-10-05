from rest_framework import serializers

from chama.models import Chama
from chama.services import ChamaClosed
from member.models import ChamaMember

from .models import Official


class OfficialSerializer(serializers.ModelSerializer):
    position = serializers.ChoiceField(
        choices=Official.Position.choices
    )

    position_display = serializers.CharField(
        source="get_position_display",
        read_only=True,
    )

    member = serializers.PrimaryKeyRelatedField(
        queryset=ChamaMember.objects.filter(is_active=True)
    )

    member_name = serializers.CharField(
        source="member.full_name",
        read_only=True,
    )

    appointed_on = serializers.DateField(
        input_formats=["iso-8601", "%d/%m/%Y"],
        required=False,
    )

    appointed_by = serializers.CharField(
        source="appointed_by.email",
        read_only=True,
        default=None,
    )

    class Meta:
        model = Official
        fields = [
            "id",
            "chama",
            "member",
            "member_name",
            "position",
            "position_display",
            "appointed_on",
            "appointed_by",
            "ended_on",
        ]

        read_only_fields = [
            "id",
            "chama",
            "appointed_by",
            "ended_on",
        ]

    def validate(self, attrs):
        chama = self.context["chama"]
        member = attrs["member"]
        position = attrs["position"]

        if chama.status == Chama.Status.CLOSED:
            raise ChamaClosed()

        if member.chama_id != chama.pk:
            raise serializers.ValidationError({
                "member": (
                    "This person is not a member of this chama."
                )
            })

        current = chama.officials.filter(
            ended_on__isnull=True
        )

        holds = current.filter(
            member=member
        ).first()

        if holds:
            raise serializers.ValidationError({
                "member": (
                    f"{member.full_name} already holds the office "
                    f"of {holds.position}."
                )
            })

        holder = (
            current
            .filter(position=position)
            .select_related("member")
            .first()
        )

        if holder and not self.context.get("replace"):
            raise serializers.ValidationError({
                "position": (
                    f"The {position} is currently "
                    f"{holder.member.full_name}. "
                    f"End that term first, or send "
                    f'"replace": true to hand the office over.'
                )
            })

        return attrs
    