# utils/emailer.py
import os

def send_email(recipient: str, subject: str, message: str):
    recipient = os.getenv("EMAIL_RECIPIENT", recipient)
    print(f"[📧 EMAIL] To: {recipient}\nSubject: {subject}\n{message}\n")