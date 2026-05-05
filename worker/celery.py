from email.mime.multipart import MIMEMultipart
import smtplib
import ssl

from celery import Celery
from app.settings import Settings


settings = Settings()

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_REDIS_URL
celery.conf.result_backend = settings.CELERY_REDIS_URL


@celery.task(name="send_email_task")
def send_email_task(msg: MIMEMultipart):
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, context=context)
    server.login(settings.from_email, settings.smtp_password)
    server.send_message(msg)
    server.quit()