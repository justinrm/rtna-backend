import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.utilities.logging import get_logger, log_event, log_exception

logger = get_logger(__name__)

class Alerts:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient_email, subject, message):
        """
        Send an email notification.
        """
        log_event(logger, "EMAIL_SEND", "Sending email", recipient_email=recipient_email, subject=subject)
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, msg.as_string())

            log_event(logger, "EMAIL_SEND", "Email sent successfully", recipient_email=recipient_email)
        except Exception as e:
            log_exception(logger, e, "Error sending email", recipient_email=recipient_email)
            raise

    def notify_admins(self, subject, message, admins):
        """
        Notify multiple admins via email.
        """
        log_event(logger, "EMAIL_NOTIFICATION", "Notifying admins", admin_count=len(admins), subject=subject)
        for admin_email in admins:
            self.send_email(admin_email, subject, message)

