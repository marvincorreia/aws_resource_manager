from django.conf import settings
from app.models import CronJob
from crontab import CronTab


cron_user = "root"
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"


def create_cronjob(cron_job: CronJob):
    cron = CronTab(user=cron_user)
    # cleanup cronjobs with the same key
    cron.remove_all(comment=str(cron_job.id))
    command = f'PATH={PATH} /bin/bash -c \'cd {settings.BASE_DIR} && python manage.py runscript app.cron.jobs.main --script-args "{cron_job.action}" "{cron_job.aws_account.name}" "{cron_job.name}" >> {settings.BASE_DIR}/cron.log 2>&1\''
    # command = f'PATH={PATH} cd {settings.BASE_DIR} && python3 manage.py runscript app.cron.run_cronjobs "{cron_job.action}" "{cron_job.aws_account.name}" "{cron_job.name}" >> {settings.BASE_DIR}/cron.log 2>&1\''

    job = cron.new(command=command)
    job.setall(
        f'{cron_job.minute} {cron_job.hour} {cron_job.day_of_month} {cron_job.month} {cron_job.day_of_week}'
    )
    job.set_comment(str(cron_job.id))
    job.enable(cron_job.active)
    cron.write()


def delete_cronjob(cron_job: CronJob):
    cron = CronTab(user=cron_user)
    cron.remove_all(comment=str(cron_job.id))
    cron.write()


def add_fetch_resources_job():
    cron = CronTab(user=cron_user)
    comment = "fetch aws resources"
    cron.remove_all(comment=comment)
    command = f'PATH={PATH} /bin/bash -c \'cd {settings.BASE_DIR} && python manage.py runscript app.cron.jobs.fetch_aws_resources >> {settings.BASE_DIR}/cron.log 2>&1\''
    job = cron.new(command=command)
    job.setall("*/30 * * * *") # fetch every 30 minutes
    job.set_comment(comment)
    job.enable(True)
    cron.write()


def config():
    cron = CronTab(user=cron_user)

    cron.remove_all()
    add_fetch_resources_job()

    for cron_job in CronJob.objects.all():
        create_cronjob(cron_job)

