import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Secure API key as described here:
# https://stackoverflow.com/questions/71504363/how-to-access-github-actions-environment-secrets-locally-and-remotely
try:  # This should run locally if config.py with key in same directory as this file
    from .config import SG_FULL_API_KEY
    API_key = SG_FULL_API_KEY
except:  # This should run on Heroku config var
    API_key = os.environ['SG_FULL_API_KEY']
# https://devcenter.heroku.com/articles/config-vars#accessing-config-var-values-from-code


def send_mail(user, subject, text):
    """
    Format and send email using SendGrid's Python Library
    https://github.com/sendgrid/sendgrid-python
    """
    message = Mail(
        from_email='mail@litewatch.co',
        to_emails=user,
        subject=subject,
        html_content=text)
    try:
        sg = SendGridAPIClient(API_key)
        response = sg.send(message)
        print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(e)
