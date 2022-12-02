import requests
import os

# Secure API key as described here:
# https://stackoverflow.com/questions/71504363/how-to-access-github-actions-environment-secrets-locally-and-remotely
try:  # This should run locally if config.py with key in same directory as this file
    from .config import API_key
    API_key = API_key
except:  # This should run on GitHub Actions
    API_key = os.environ['MAILGUN_API_KEY']
# If this doesn't work, try Heroku Config Vars. This could be in second try/except block. See details at:
# https://devcenter.heroku.com/articles/config-vars#accessing-config-var-values-from-code

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
