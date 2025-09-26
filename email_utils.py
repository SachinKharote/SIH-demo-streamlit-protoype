# email_utils.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = "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"  # replace with your key
FROM_EMAIL = "ksach320@gmail.com"  # must be verified in SendGrid

def send_registration_email(to_email, name):
    """
    Sends a registration confirmation email via SendGrid.
    Returns True if email sent successfully, False otherwise.
    """
    try:
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=to_email,
            subject="Registration Confirmation",
            html_content=f"<p>Hello {name},</p><p>Your registration was successful!</p>"
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        # 202 = accepted
        return response.status_code == 202
    except Exception as e:
        print(f"Email send error: {e}")
        return False
