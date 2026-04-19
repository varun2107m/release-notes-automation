import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()


def send_email(subject, body, recipients):
    sender = os.getenv("EMAIL")
    password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender or not password:
        raise Exception("Missing EMAIL or EMAIL_APP_PASSWORD in .env")

    if not recipients:
        raise Exception("Recipient list is empty")

    # Create email
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())
        server.quit()

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Failed to send email:", str(e))
        raise
    