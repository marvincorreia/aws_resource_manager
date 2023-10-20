from django.conf import settings
from app.models import CronJob
from crontab import CronTab


cron_user = "root"


def create_cronjob(cron_job: CronJob):
    cron = CronTab(user=cron_user)
    # cleanup cronjobs with the same key
    cron.remove_all(comment=str(cron_job.id))
    PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    command = f'PATH={PATH} /bin/bash -c \'cd {settings.BASE_DIR} && python manage.py runscript app.cron.run_cronjobs --script-args "{cron_job.action}" "{cron_job.aws_account.name}" "{cron_job.name}" >> {settings.BASE_DIR}/cron.log 2>&1\''
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


def run():
    # cron_file_path = settings.BASE_DIR / 'cron.tab'

    # with open(cron_file_path, 'w') as file:
    #     file.write("")
    #     print(f"File '{cron_file_path}' has been created.")
    
    # cron = CronTab(tabfile=cron_file_path)
    cron = CronTab(user=cron_user)

    cron.remove_all()

    for cron_job in CronJob.objects.all():
        create_cronjob(cron_job)

