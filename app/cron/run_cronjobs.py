from app import models
from app.awsdk import ec2_perform_action, rds_perform_action


def run(*args):
    action = args[0]
    account_name = args[1]
    cronjob_name = args[2]

    aws_account = models.AWSAccount.objects.get(name=account_name)
    cronjob = models.CronJob.objects.get(name=cronjob_name)
    instances_names = [x.instance_name for x in aws_account.ec2_instances.filter(managed=True)] + [x.db_identifier for x in aws_account.rds_instances.filter(managed=True)]
    description = f"{action} instances {', '.join(instances_names)}"
    log_data = ""

    try:
        ec2_response = ec2_perform_action(aws_account, action)
        rds_response = rds_perform_action(aws_account, action)
        log_data = str(ec2_response) + '\n\n' + str(rds_response)
        success = True
    except Exception as e:
        log_data = f'{e}'
        success = False

    models.CronJobLog.objects.create(cronjob=cronjob, description=description, log_data=f'{log_data}', success=success)

