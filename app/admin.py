from django.contrib import admin, messages
from . import models
from .forms import AWSAccountForm, NotificationForm
from .awsdk import get_aws_ec2_instances, get_aws_rds_instances, ec2_perform_action, rds_perform_action
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
    list_display.insert(1, 'up')
    list_filter = ('aws_account', 'managed', 'instance_state')
    search_fields = [x.name for x in models.EC2Instance._meta.fields if x.name not in ['aws_account',]]

    actions = ['start_ec2_instances', 'stop_ec2_instances', 'enable_managed', 'disable_managed']

    def start_ec2_instances(self, request, queryset):
        r = ec2_perform_action(queryset, 'up')
        self.message_user(request, ", ".join(r), messages.INFO)

    def stop_ec2_instances(self, request, queryset):
        r = ec2_perform_action(queryset, 'down')
        self.message_user(request, ", ".join(r), messages.INFO)

    def enable_managed(self, request, queryset):
        queryset.update(managed=True)

    def disable_managed(self, request, queryset):
        queryset.update(managed=False)

    start_ec2_instances.short_description = "Start selected"
    stop_ec2_instances.short_description =  "Stop selected"
    enable_managed.short_description = "Allow cronjob for selected (managed)"
    disable_managed.short_description = "Disallow cronjob for selected (managed)"


@admin.decorators.register(models.RDSInstance)
class RDSInstanceAdmin(admin.ModelAdmin):
    list_display = [x.name for x in models.RDSInstance._meta.fields if x.name not in ['id',]]
    list_display.insert(1, 'up')
    list_filter = ('aws_account', 'managed')
    search_fields = [x.name for x in models.RDSInstance._meta.fields if x.name not in ['aws_account',]]
    actions = ['start_rds_instances', 'stop_rds_instances', 'enable_managed', 'disable_managed']

    def start_rds_instances(self, request, queryset):
        r = rds_perform_action(queryset, 'up')
        self.message_user(request, ", ".join(r), messages.INFO)

    def stop_rds_instances(self, request, queryset):
        r = rds_perform_action(queryset, 'down')
        self.message_user(request, ", ".join(r), messages.INFO)

    def enable_managed(self, request, queryset):
        queryset.update(managed=True)

    def disable_managed(self, request, queryset):
        queryset.update(managed=False)

    start_rds_instances.short_description = "Start selected"
    stop_rds_instances.short_description =  "Stop selected"
    enable_managed.short_description = "Allow cronjob for selected (managed)"
    disable_managed.short_description = "Disallow cronjob for selected (managed)"



@admin.decorators.register(models.CronJob)
class CronJobAdmin(admin.ModelAdmin):
    list_display = [x.name for x in models.CronJob._meta.fields if x.name not in ['id',]]
    list_filter = ('aws_account',)
    # inlines = [admin_inlines.CronJobLogInline,]
    actions = ['activate', 'deactivate', 'duplicate']

    def duplicate(self, request, queryset):
        for i in queryset:
            i.pk = None
            i.name = f"copy of {i.name}"
            i.active = False
            i.save()
            self.message_user(request, f"{i.name} created", messages.INFO)

    def activate(self, request, queryset):
        for i in queryset:
            i.active = True
            i.save()

    def deactivate(self, request, queryset):
        for i in queryset:
            i.active = False
            i.save()

    activate.short_description = "Activate selected"
    deactivate.short_description = "Deactivate selected"
    duplicate.short_description = "Duplicate selected"



@admin.decorators.register(models.CronJobLog)
class CronJobLogAdmin(admin.ModelAdmin):
    list_display = [x.name for x in models.CronJobLog._meta.fields if x.name not in ['id', 'log_data']]
    

@admin.decorators.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [x.name for x in models.Notification._meta.fields if x.name not in ['id', 'auth_password', 'tls', 'ssl', 'auth_user']]
    # form = NotificationForm
    actions = ["duplicate"]

    def duplicate(self, request, queryset):
        for i in queryset:
            i.pk = None
            i.subject = f"copy of {i.subject}"
            i.active = False
            i.save()
            self.message_user(request, f"{i.subject} created", messages.INFO)

    duplicate.short_description = "Duplicate selected"

