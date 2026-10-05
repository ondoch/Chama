from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from access.services import record_audit
from member.models import ChamaMember

from .models import Official


@receiver(post_save, sender=ChamaMember)
def end_offices_of_removed_member(sender, instance, **kwargs):
    if instance.is_active:
        return
    for office in Official.objects.filter(member=instance, ended_on__isnull=True).select_related("chama"):
        office.ended_on = timezone.localdate()
        office.save(update_fields=["ended_on"])
        record_audit(None, "official.ended", office.pk, f"{instance.full_name} ({office.chama.name})",
                     {"chama": office.chama.name, "position": office.position, "reason": "member removed"})
