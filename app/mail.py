from app.models import AWSAccount, CronJobLog, Notification
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend


def send(aws_account: AWSAccount, job_log: CronJobLog):
    notifications = aws_account.notification_configs.filter(active=True)

    if not notifications:
        return
    
    notification: Notification = notifications[0]

    if job_log.success and notification.only_failed_jobs:
        return

    try:
        body = f"Description: {job_log.description}\n" \
        f"Cronjob: {job_log.cronjob}\n" \
        f"Success: {job_log.success}\n" \
        f"Log data: {job_log.log_data}\n" \
        f"Time: {job_log.time}\n"

        backend = EmailBackend(
            host=notification.server, 
            port=notification.port, 
            username=notification.auth_user, 
            password=notification.auth_password, 
            use_tls=notification.tls, 
            use_ssl=notification.ssl, 
            fail_silently=False)
        
        email = EmailMessage(
            subject=notification.subject, 
            body=body, 
            from_email=notification.from_email,
            reply_to=[notification.from_email,],
            to=[x.strip() for x in notification.recipient_list.split(",")],
            connection=backend)
        
        email.send()
    except Exception as e:
        print(e)
    