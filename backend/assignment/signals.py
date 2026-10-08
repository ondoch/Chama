from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from access.services import record_audit
from chama.models import Chama
from chama.serializers import employee_code
from employee.models import Employee

from .models import Assignment


@receiver(post_save, sender=Chama)
def assign_creator_to_new_chama(sender, instance, created, **kwargs):
    if created and instance.created_by_id:
        Assignment.objects.create(
            chama=instance,
            employee=instance.created_by,
            assigned_by=instance.created_by.user,
        )


@receiver(post_save, sender=Employee)
def release_chamas_of_terminated_employee(sender, instance, **kwargs):
    if instance.status:
        return

    for assignment in Assignment.objects.filter(
        employee=instance, unassigned_at__isnull=True
    ).select_related("chama"):
        assignment.unassigned_at = timezone.now()
        assignment.save(update_fields=["unassigned_at"])
        record_audit(
            None,
            "chama.auto_unassigned",
            assignment.chama_id,
            assignment.chama.chama_name,
            {
                "employee": employee_code(instance),
                "reason": "employee terminated",
            },
        )