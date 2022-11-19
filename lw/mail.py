import requests
mailgun_sender = 'sandbox5243c587fa544caa9915e96ddd99a4cd.mailgun.org'
API_key = '716ca4acc5bc42510a53de7f515f5aab-2de3d545-89158eb8'
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
