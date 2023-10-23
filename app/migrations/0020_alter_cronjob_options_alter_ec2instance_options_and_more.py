# Generated by Django 4.2.6 on 2023-10-23 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_cronjoblog_options_alter_ec2instance_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cronjob',
            options={'ordering': ['-active'], 'verbose_name': 'Cron Job', 'verbose_name_plural': 'Cron Jobs'},
        ),
        migrations.AlterModelOptions(
            name='ec2instance',
            options={'default_related_name': 'ec2_instances', 'ordering': ['-launch_time'], 'verbose_name': 'AWS EC2 Instance', 'verbose_name_plural': 'AWS EC2 Instances'},
        ),
        migrations.AlterModelOptions(
            name='rdsinstance',
            options={'default_related_name': 'rds_instances', 'ordering': ['-creation_time'], 'verbose_name': 'AWS RDS Instance', 'verbose_name_plural': 'AWS RDS Instances'},
        ),
        migrations.AlterField(
            model_name='awsaccount',
            name='aws_secret_access_key',
            field=models.CharField(help_text='This field is not visible for security reasons', max_length=100),
        ),
    ]