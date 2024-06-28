from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management import call_command
from .models import Report


@receiver(post_save, sender=Report)
def run_populate_data(sender, instance, created, **kwargs):
    if created:
        call_command('populate_data', instance.file.path)



