from app import models
from app.awsdk import ec2_perform_action, rds_perform_action
import app.mail

def run(*args):
    action = args[0]
    account_name = args[1]
    cronjob_name = args[2]

    aws_account = models.AWSAccount.objects.get(name=account_name)
    cronjob = models.CronJob.objects.get(name=cronjob_name)
    ec2_instances = aws_account.ec2_instances.filter(managed=True)
    rds_instances = aws_account.rds_instances.filter(managed=True)
    instances_names = [x.instance_name for x in ec2_instances] + [x.db_identifier for x in rds_instances]
    description = f"{action} instances {', '.join(instances_names)}"
    log_data = ""

    try:
        ec2_response = ec2_perform_action(ec2_instances, action)
        rds_response = rds_perform_action(rds_instances, action)
        log_data = "\n".join(ec2_response + rds_response)
        success = False  if "error" in log_data.lower() else True 
    except Exception as e:
        print(e)
        log_data = f'{e}'
        success = False

    job_log = models.CronJobLog.objects.create(cronjob=cronjob, description=description, log_data=f'{log_data}', success=success)

    app.mail.send(aws_account, job_log)
