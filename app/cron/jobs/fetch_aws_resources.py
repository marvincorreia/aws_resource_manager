from app.awsdk import get_aws_ec2_instances, get_aws_rds_instances
from app.models import AWSAccount


def run():
    for account in AWSAccount.objects.all():
        try:
            get_aws_ec2_instances(account)
            get_aws_rds_instances(account)
        except Exception as e:
            print(e)
