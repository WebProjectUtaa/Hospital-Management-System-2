import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    @staticmethod
    def send_email(to_email, subject, message):
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "alilivanturk@gmail.com"  
        sender_password = os.getenv("EMAIL_PASSWORD")

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                print(f"Email sent to {to_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

