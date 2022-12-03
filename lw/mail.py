import requests
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

"""     # this approach with mailgun worked, but an API policy forces us to use a different provider
mailgun_sender = 'sandbox5243c587fa544caa9915e96ddd99a4cd.mailgun.org'
API_base_URL = 'https://api.mailgun.net/v3/sandbox5243c587fa544caa9915e96ddd99a4cd.mailgun.org'
API_path = API_base_URL + '/messages'
sender_address = 'sandbox5243c587fa544caa9915e96ddd99a4cd@mailgun.org'

def send_mail(user, subject, text):
    return requests.post(
        API_path,
        auth=("api", API_key),
        data={"from": sender_address,
              "to": [user],
              "subject": subject,
              "text": text})
"""

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python


def send_mail(user, subject, text):
    message = Mail(
        from_email='mail@litewatch.co',
        to_emails=user,
        subject=subject,
        html_content=text)
    try:
        sg = SendGridAPIClient(API_key)
        response = sg.send(message)
        print(response.status_code)
        #print(response.body)
        #print(response.headers)
    except Exception as e:
        print(e)
