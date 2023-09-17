from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

def send_custom_email(recipient_email, reset_link):
  message = Mail(
    from_email=os.environ.get('SENDGRID_SENDER_EMAIL'),
    to_emails=recipient_email,
    subject='Password Reset',
    html_content=f'<strong>Click this link to reset your password: {reset_link}</strong>'
  )

  try:
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
  except Exception as e:
    print(e)