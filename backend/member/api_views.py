from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from access.services import record_audit
from authentication.permissions import PasswordUpToDate
from chama.models import Chama
from chama.services import ChamaClosed, scoped_chamas

from .permissions import MemberPermission
from .serializers import MemberSerializer

TRUE = ("1", "true", "True")


class MemberViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = MemberSerializer
    permission_classes = [PasswordUpToDate, MemberPermission]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.chama = get_object_or_404(scoped_chamas(request.user), pk=kwargs["chama_pk"])

    def get_serializer_context(self):
        return {**super().get_serializer_context(), "chama": self.chama}

    def get_queryset(self):
        qs = self.chama.members.prefetch_related("offices")
        if self.action == "list" and self.request.query_params.get("include_removed") not in TRUE:
            qs = qs.filter(is_active=True)
        return qs

    def _audit(self, action_name, member, details=None):
        record_audit(self.request.user, action_name, member.pk, f"{member.full_name} ({self.chama.name})",
                     {"chama": self.chama.name, **(details or {})})

    def perform_create(self, serializer):
        member = serializer.save(chama=self.chama)
        self._audit("member.added", member)

    def perform_update(self, serializer):
        fields = ("full_name", "phone", "email", "joined_on", "national_id")
        before = {f: str(getattr(serializer.instance, f)) for f in fields}
        member = serializer.save()
        changes = {f: ("changed" if f == "national_id" else [before[f], str(getattr(member, f))])
                   for f in fields if before[f] != str(getattr(member, f))}
        if changes:
            self._audit("member.updated", member, changes)

    def destroy(self, request, *args, **kwargs):
        member = self.get_object()
        if self.chama.status == Chama.Status.CLOSED:
            raise ChamaClosed()
        if not member.is_active:
            raise ValidationError("This member has already been removed.")
        member.is_active = False
        member.removed_at = timezone.now()
        member.save(update_fields=["is_active", "removed_at"])
        self._audit("member.removed", member)
        return Response(status=status.HTTP_204_NO_CONTENT)
