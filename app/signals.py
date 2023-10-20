from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from . import models
from .cron.config import create_cronjob, delete_cronjob


@receiver(post_save, sender=models.CronJob)
def cron_job_post_save(sender, instance, **kwargs):
    create_cronjob(instance)

@receiver(post_delete, sender=models.CronJob)
def cron_job_post_delete(sender, instance, **kwargs):
    delete_cronjob(instance)
