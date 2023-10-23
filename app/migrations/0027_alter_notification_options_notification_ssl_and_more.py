# Generated by Django 4.2.6 on 2023-10-23 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_notification_port_notification_server_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'default_related_name': 'notification_configs', 'verbose_name': 'Notification', 'verbose_name_plural': 'Notifications'},
        ),
        migrations.AddField(
            model_name='notification',
            name='ssl',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='tls',
            field=models.BooleanField(default=False),
        ),
    ]
