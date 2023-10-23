from django.db import models
from django.urls import reverse
from django.utils import timezone
import uuid


ACTIONS = (
    ('up', 'UP'),
    ('down', 'DOWN'),
)


class AWSAccount(models.Model):
    name = models.CharField(max_length=20, unique=True)
    aws_access_key_id = models.CharField(max_length=50)
    aws_secret_access_key = models.CharField(max_length=100, help_text='This field is not visible for security reasons')
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'AWS Account'
        verbose_name_plural = 'AWS Accounts'


class EC2Instance(models.Model):
    instance_id = models.CharField(max_length=20, primary_key=True)
    instance_name = models.CharField(max_length=100)
    instance_state = models.CharField(max_length=20)
    instance_type = models.CharField(max_length=20)
    platform = models.CharField(max_length=20)
    public_ip = models.GenericIPAddressField(null=True, blank=True)
    launch_time = models.DateTimeField()
    aws_account = models.ForeignKey(AWSAccount, on_delete=models.CASCADE)
    managed = models.BooleanField(default=False, help_text="If selected cronjob can manage this resource")

    class Meta:
        verbose_name = 'AWS EC2 Instance'
        verbose_name_plural = 'AWS EC2 Instances'
        default_related_name = 'ec2_instances'
        ordering = ['-launch_time']

    def __str__(self):
        return self.instance_name
    
    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    
    def up(self):
        return not self.instance_state.lower().startswith('stop')
    
    up.boolean = True


class RDSInstance(models.Model):
    db_identifier = models.CharField(max_length=100, primary_key=True)
    db_engine = models.CharField(max_length=20)
    db_status = models.CharField(max_length=20)
    db_instance_class = models.CharField(max_length=20)
    creation_time = models.DateTimeField()
    aws_account = models.ForeignKey(AWSAccount, on_delete=models.CASCADE)
    managed = models.BooleanField(default=False, help_text="If selected cronjob can manage this resource")

    class Meta:
        verbose_name = 'AWS RDS Instance'
        verbose_name_plural = 'AWS RDS Instances'
        default_related_name = 'rds_instances'
        ordering = ['-creation_time']

    def __str__(self):
        return self.db_identifier
    
    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    
    def up(self):
        return not self.db_status.lower().startswith('stop')
    
    up.boolean = True


class CronJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    aws_account = models.ForeignKey(AWSAccount, on_delete=models.CASCADE)
    action = models.CharField(choices=ACTIONS, max_length=5, blank=False, null=False)

    minute = models.CharField(max_length=10, default='0', help_text='min (0-59) or * for every minute')
    hour = models.CharField(max_length=10, default='0', help_text='hour (0-23) or *  for every hour')
    day_of_month = models.CharField(max_length=10, default='*', help_text='1-31 or * for all day of month')
    month = models.CharField(max_length=10, default='*', help_text='1-12 or * for all months')
    day_of_week = models.CharField(max_length=10, default='*', help_text='0-6 (sunday to saturday) or * for all week days')
    active =  models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cron Job'
        verbose_name_plural = 'Cron Jobs'
        ordering = ['-active']


class CronJobLog(models.Model):
    time = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=200, default="")
    log_data = models.TextField()
    cronjob = models.ForeignKey(CronJob, on_delete=models.CASCADE)
    success = models.BooleanField(default=True)

    # def __str__(self):
    #     self.description

    class Meta:
        verbose_name = 'Job Log'
        verbose_name_plural = 'Job Logs'
        ordering = ['-time']


class Notification(models.Model):
    subject = models.CharField(max_length=100)
    aws_account = models.ForeignKey(AWSAccount, on_delete=models.CASCADE)
    from_email = models.EmailField()
    recipient_list = models.TextField(help_text="separated with a comma (,)")
    server = models.CharField(max_length=50, default="smtp.gmail.com")
    port = models.IntegerField(default=587)
    auth_user = models.EmailField()
    auth_password = models.CharField(max_length=100, help_text='This field is not visible for security reasons')
    tls = models.BooleanField(default=True)
    ssl = models.BooleanField(default=False)
    only_failed_jobs = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
  
    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        default_related_name = 'notification_configs'

