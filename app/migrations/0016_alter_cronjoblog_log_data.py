# Generated by Django 4.2.6 on 2023-10-19 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_cronjoblog_log_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cronjoblog',
            name='log_data',
            field=models.TextField(),
        ),
    ]
