# Generated by Django 4.2.6 on 2023-10-18 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_status_cronjob_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cronjob',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
