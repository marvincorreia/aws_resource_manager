# Generated by Django 4.2.6 on 2023-10-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_alter_notification_options_notification_ssl_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='only_failed_jobs',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notification',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='tls',
            field=models.BooleanField(default=True),
        ),
    ]
