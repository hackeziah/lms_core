import time
from celery import shared_task
from lms_core.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

@shared_task
def add(x, y):
    return x + y

@shared_task
def send_email_task(self):
    subject = 'Helo from Celery'
    message = 'This is a test email sent asynchronously with Celery.'
    send_mail(
        subject,
        message,
        'lamadridkevinpaul.dev@gmail.com',
        ['lamadridkevinpaul@gmail.com'],
        fail_silently=False
    )
    return True

@shared_task
def send_email(email):
    "background task to send an email asynchronously"
    subject = 'Helo from Celery'
    message = 'This is a test email sent asynchronously with Celery.'
    
    time.sleep(5)
    return send_mail(
        subject,
        message,
        'lamadridkevinpaul.dev@gmail.com',
        [email],
        fail_silently=False
    )
# @task(name='send_otp_mail')
# def send(data: str):
#     time.sleep(5)
#     return send_mail(
#         'Subject here',
#         f'{data}',
#         'lamadridkevinpaul.dev@gmail.com',
#         ['lamadridkevinpaul@gmail.com'],
#         fail_silently=False,
#     )
    


# # def sending():
# #     send.delay("hello Kevin")
# #     return True
