from config.celery import app
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@app.task
def send_otp_email_task(subject, otp_code, recipient):
    send_mail(subject, f'Your login code is: {otp_code}', settings.EMAIL_HOST_USER, [recipient],
              fail_silently=False)