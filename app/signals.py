from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib import messages
from . import models
from .cron import create_cronjob, delete_cronjob
from app.awsdk import get_aws_ec2_instances, get_aws_rds_instances


@receiver(post_save, sender=models.CronJob)
def cron_job_post_save(sender, instance, **kwargs):
    create_cronjob(instance)


@receiver(post_delete, sender=models.CronJob)
def cron_job_post_delete(sender, instance, **kwargs):
    delete_cronjob(instance)


@receiver(post_save, sender=models.AWSAccount)
def aws_account_post_save(sender, instance, created, **kwargs):
    if created:
        try:
            get_aws_ec2_instances(instance)
            get_aws_rds_instances(instance)
        except Exception as e:
            pass

