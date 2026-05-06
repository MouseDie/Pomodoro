from worker.celery import send_email_task


class MailClient:
    
    @staticmethod         
    def send_welcome_email(to: str) -> None:
        print(send_email_task.delay(f"Welcome email", f"welcome to pomodoro", to))

        
    

    