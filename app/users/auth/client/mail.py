import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.settings import Settings
from worker.celery import send_email_task


class MailClient:
    def __init__(self, settings: Settings):
        self.from_email = settings.from_email
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_password = settings.SMTP_PASSWORD
        
        
    def send_welcome_email(self, to: str) -> None:
        msg = self.__build_message(f"Welcome email", f"Welcome to pomodoro", to)
        self.__send_message(msg)
        
    
    def __build_message(self, subject: str, text: str, to: str) -> MIMEMultipart:
        msg = MIMEMultipart()
        
        msg["From"] = self.from_email
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(text, "plain"))
        return msg
    
    
    @staticmethod
    def __send_message(msg: MIMEMultipart) -> None:
        task_id = send_email_task.delay(msg)
        return task_id
    
    