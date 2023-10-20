import boto3
from . import models

def get_aws_ec2_instances(aws_account: models.AWSAccount):
   
    # Initialize the AWS EC2 client with your credentials
    ec2 = boto3.client('ec2', 
                    region_name='us-east-1',  # Replace with your desired region
                    aws_access_key_id=aws_account.aws_access_key_id,
                    aws_secret_access_key=aws_account.aws_secret_access_key)

    # Use the `describe_instances` method to list EC2 instances
    response = ec2.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:

            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']
            instance_type = instance['InstanceType']
            platform = instance.get('Platform', 'Linux')
            public_ip = instance.get('PublicIpAddress', 'N/A')
            launch_time = instance['LaunchTime']
            instance_name = ''

            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']
            
            defauts = dict(
                instance_name = instance_name,
                instance_state = instance_state,
                instance_type = instance_type,
                platform = platform,
                public_ip = public_ip,
                launch_time = launch_time,
            )

            obj, created = models.EC2Instance.objects.update_or_create(
                instance_id = instance_id,
                aws_account = aws_account,
                defaults=defauts
            )

            if created:
                print(f"{obj} created")
            else:
                print(f"{obj} updated")
            
            # print(f"Instance ID: {instance_id}, Name: {instance_name}, State: {instance_state}, Type: {instance_type}, Platform: {platform}, Public IP: {public_ip}, Launch Time: {launch_time}")


def get_aws_rds_instances(aws_account: models.AWSAccount):
    # Initialize the AWS RDS client with your credentials
    rds = boto3.client('rds',
                    region_name='us-east-1',  # Replace with your desired region
                    aws_access_key_id=aws_account.aws_access_key_id,
                    aws_secret_access_key=aws_account.aws_secret_access_key)

    # Use the `describe_db_instances` method to list RDS instances
    response = rds.describe_db_instances()

    for db_instance in response['DBInstances']:
        # Extract and print RDS details
        db_identifier = db_instance['DBInstanceIdentifier']
        db_engine = db_instance['Engine']
        db_status = db_instance['DBInstanceStatus']
        db_instance_class = db_instance['DBInstanceClass']
        creation_time = db_instance['InstanceCreateTime']

        defauts = dict(
            db_engine = db_engine,
            db_status = db_status,
            db_instance_class = db_instance_class,
            creation_time = creation_time,
        )

        obj, created = models.RDSInstance.objects.update_or_create(
            db_identifier = db_identifier,
            aws_account = aws_account,
            defaults=defauts
        )

        if created:
            print(f"{obj} created")
        else:
            print(f"{obj} updated")
        
        # print(f"DB Identifier: {db_identifier}, Engine: {db_engine}, Status: {db_status}, Instance Class: {db_instance_class}, Creation Time: {creation_time}")


def ec2_perform_action(aws_account: models.AWSAccount, action: str):
    ec2 = boto3.client('ec2', 
                    region_name='us-east-1',  # Replace with your desired region
                    aws_access_key_id=aws_account.aws_access_key_id,
                    aws_secret_access_key=aws_account.aws_secret_access_key)
    
    instances_ids = [x.instance_id for x in aws_account.ec2_instances.filter(managed=True)]
    
    if action.lower() == "up":
        response = ec2.start_instances(InstanceIds=instances_ids, DryRun=False)
    elif action.lower() == "down":
        response = ec2.stop_instances(InstanceIds=instances_ids, DryRun=False)
   
    return response


def rds_perform_action(aws_account: models.AWSAccount,  action: str):
    rds = boto3.client('rds', 
                    region_name='us-east-1',  # Replace with your desired region
                    aws_access_key_id=aws_account.aws_access_key_id,
                    aws_secret_access_key=aws_account.aws_secret_access_key)
    
    rds_instances = aws_account.rds_instances.filter(managed=True)
    responses = []

    for i in rds_instances :
        try:
            if action.lower() == "up":
                response = rds.start_db_instance(DBInstanceIdentifier=i.db_identifier)
                responses.append(response)
            elif action.lower() == "down":
                response = rds.stop_db_instance(DBInstanceIdentifier=i.db_identifier)
                responses.append(response)
        except Exception as e:
            responses.append({'ERROR': f"{i} - {e}"})
    
    return responses