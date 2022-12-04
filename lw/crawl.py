import requests
from bs4 import BeautifulSoup
import re
from .mail import send_mail


def collect(url, search_word, elem_type, elem_attr):
    """
    This function performs the webscraping for the project.
    Called from cron.py and views.py
    """
    try:
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        body = soup.body

        field = body.find_all(elem_type, attrs={'class', elem_attr})
        found = []
        for f in field:
            if f.find_all('p', string=re.compile(search_word)):
                anchor = f.find('a')
                found.append((anchor.get('title'), anchor['href']))
                # found.append((anchor['href'], anchor.get('title')))
                # the old way. Delete once the new way works

        return found
    except Exception as e:
        print(e)
        return False


def test_search(email_address, url, search_word, elem_type, elem_attr):
    """
    Simplified version of cron.py to be run from "Create New Search" page.
    This could be relocated to a different part of the codebase if desired.
    """
    found_word = collect(url, search_word, elem_type, elem_attr)
    if found_word:
        message_html = ''
        for f in found_word:
            message_html += '<h3>' + f[0] + '</h3>'
            link = '<a clicktracking="off" href="' + f[1] + '">'
            message_html += link + f[1] + '</a>'
        if message_html:
            success_message = 'Great news! We found results in your search for ' \
                              '"{}" at {}\n'.format(search_word, url)
            success_message += message_html
            send_mail(email_address, search_word, success_message)
