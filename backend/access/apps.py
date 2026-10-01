from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_role_groups(sender, **kwargs):
    from django.contrib.auth.models import Group

    from .catalog import ROLES

    for _key, label, _perms in ROLES:
        Group.objects.get_or_create(name=label)

class AccessConfig(AppConfig):
    name = 'access'

    def ready(self):
        post_migrate.connect(create_role_groups, sender=self)
