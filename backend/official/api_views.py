from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from access.services import record_audit
from authentication.permissions import PasswordUpToDate
from chama.models import Chama
from chama.services import ChamaClosed, scoped_chamas

from .models import Official
from .permissions import OfficialPermission
from .serializers import OfficialSerializer

TRUE = ("1", "true", "True")


class OfficialViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = OfficialSerializer
    permission_classes = [PasswordUpToDate, OfficialPermission]
    pagination_class = None

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)           # login + permissions first
        self.chama = get_object_or_404(
            scoped_chamas(request.user), public_id=kwargs["chama_pk"]
        )

    def get_serializer_context(self):
        replace = self.request.data.get("replace") in (True, "true", "True", "1", 1) if self.request else False
        return {**super().get_serializer_context(), "chama": self.chama, "replace": replace}

    def get_queryset(self):
        qs = self.chama.officials.select_related("member", "appointed_by")
        if self.action == "list" and self.request.query_params.get("include_past") not in TRUE:
            qs = qs.filter(ended_on__isnull=True)
        return qs

    def _audit(self, action_name, official, details=None):
        chama_name = self.chama.chama_name
        record_audit(self.request.user, action_name, official.pk,
                     f"{official.member.full_name} ({chama_name})",
                     {"chama": chama_name, "position": official.position, **(details or {})})

    @transaction.atomic
    def perform_create(self, serializer):
        position = serializer.validated_data["position"]
        if self.get_serializer_context()["replace"]:
            for old in self.chama.officials.filter(position=position, ended_on__isnull=True).select_related("member"):
                old.ended_on = timezone.localdate()
                old.save(update_fields=["ended_on"])
                self._audit("official.ended", old, {"reason": "replaced"})
        official = serializer.save(chama=self.chama, appointed_by=self.request.user)
        self._audit("official.appointed", official)

    def destroy(self, request, *args, **kwargs):
        official = self.get_object()
        if self.chama.status == Chama.Status.CLOSED:
            raise ChamaClosed()
        if official.ended_on is not None:
            raise ValidationError("This term has already ended.")
        official.ended_on = timezone.localdate()
        official.save(update_fields=["ended_on"])
        self._audit("official.ended", official, {"reason": "term ended"})
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def replace_all(self, request, *args, **kwargs):
        """PUT {"officials": {"chairperson": 3|null, "secretary": 5|null, "treasurer": 8|null}}"""
        if self.chama.status == Chama.Status.CLOSED:
            raise ChamaClosed()

        selection = request.data.get("officials")
        positions = {p.value for p in Official.Position}
        if not isinstance(selection, dict) or set(selection) != positions:
            raise ValidationError("Provide all three positions: chairperson, secretary, treasurer.")

        ids = [mid for mid in selection.values() if mid is not None]
        if len(ids) != len(set(ids)):
            raise ValidationError("A member can hold only one office.")

        members = {m.id: m for m in self.chama.members.filter(is_active=True, id__in=ids)}
        if set(ids) - set(members):
            raise ValidationError("Every official must be an active member of this chama.")

        today = timezone.localdate()
        current = {o.position: o for o in
                   self.chama.officials.filter(ended_on__isnull=True).select_related("member")}

        # free every changed seat first, so swaps don't hit the unique constraints
        for pos, old in current.items():
            if old.member_id != selection[pos]:
                old.ended_on = today
                old.save(update_fields=["ended_on"])
                self._audit("official.ended", old, {"reason": "replaced"})

        for pos, mid in selection.items():
            if mid is None or (pos in current and current[pos].member_id == mid):
                continue
            official = Official.objects.create(
                chama=self.chama, member=members[mid], position=pos,
                appointed_by=request.user,
            )
            self._audit("official.appointed", official)

        qs = self.chama.officials.filter(ended_on__isnull=True).select_related("member", "appointed_by")
        return Response(self.get_serializer(qs, many=True).data)
    