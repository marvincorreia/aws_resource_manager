from django.contrib import admin, messages
from . import models
from .forms import AWSAccountForm
from .awsdk import get_aws_ec2_instances, get_aws_rds_instances
from . import admin_inlines


@admin.decorators.register(models.AWSAccount)
class AWSAccountAdmin(admin.ModelAdmin):
    list_display = [x.name for x in models.AWSAccount._meta.fields if x.name not in ['id', 'aws_secret_access_key']]
    form = AWSAccountForm
    actions = ['fetch_resources',]
    group = "Custom Group Label"
    short_description = "My Custom Group"

    def fetch_resources(self, request, queryset):
        for i in queryset:
            try:
                get_aws_ec2_instances(aws_account=i)
                get_aws_rds_instances(aws_account=i)
                self.message_user(request, f'{i.name} - Successfully fetched AWS resources', messages.SUCCESS)
            except Exception as e:
                self.message_user(request, f'{i.name} - {e}', messages.ERROR)

    fetch_resources.short_description = "Fetch resources for selected AWS Accounts"


@admin.decorators.register(models.EC2Instance)
class EC2InstanceAdmin(admin.ModelAdmin):
    list_display = [x.name for x in models.EC2Instance._meta.fields if x.name not in ['instance_id',]]
    list_display.insert(1, 'running')
    list_filter = ('aws_account', 'managed')

    actions = ['enable_managed', 'disable_managed']

    def enable_managed(self, request, queryset):
        queryset.update(managed=True)

    def disable_managed(self, request, queryset):
        queryset.update(managed=False)

    enable_managed.short_description = "Enable 'managed' for selected EC2 instances"
    disable_managed.short_description = "Disable 'managed' for selected EC2 instances"


@admin.decorators.register(models.RDSInstance)
class RDSInstanceAdmin(admin.ModelAdmin):
    list_display = [x.name for x in models.RDSInstance._meta.fields if x.name not in ['id',]]
    list_display.insert(2, 'available')
    list_filter = ('aws_account', 'managed')

    actions = ['enable_managed', 'disable_managed']

    def enable_managed(self, request, queryset):
        queryset.update(managed=True)

    def disable_managed(self, request, queryset):
        queryset.update(managed=False)

    enable_managed.short_description = "Enable 'managed' for selected RDS instances"
    disable_managed.short_description = "Disable 'managed' for selected RDS instances"



@admin.decorators.register(models.CronJob)
class CronJobAdmin(admin.ModelAdmin):
    list_display = [x.name for x in models.CronJob._meta.fields if x.name not in ['id',]]
    list_filter = ('aws_account',)
    inlines = [admin_inlines.CronJobLogInline,]
    actions = ['activate', 'deactivate']

    def activate(self, request, queryset):
        # queryset.update(active=True)
        for i in queryset:
            i.active = True
            i.save()

    def deactivate(self, request, queryset):
        # queryset.update(active=False)
        for i in queryset:
            i.active = False
            i.save()

    activate.short_description = "Activate selected Cron Jobs"
    deactivate.short_description = "Deactivate selected Cron Jobs"


@admin.decorators.register(models.CronJobLog)
class CronJobLogAdmin(admin.ModelAdmin):
    list_display = [x.name for x in models.CronJobLog._meta.fields if x.name not in ['id', 'log_data']]
    
