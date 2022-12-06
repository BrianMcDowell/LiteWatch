import requests
from bs4 import BeautifulSoup
import re
from .mail import send_mail


def collect(url: str, search_word: str, elem_type: str = 'div', elem_attr: str = None):
    """
    This function performs the webscraping for the project.
    Called from cron.py and views.py
    """
    try:
        soup = BeautifulSoup(requests.get(url, allow_redirects=True, timeout=10).text, "html.parser")
        body = soup.body
        selector = elem_type
        if elem_attr:
            selector += "." + elem_attr
        field = body.select(selector)
        found = []
        for f in field:
            if f.find_all(string=re.compile(search_word)):
                anchor = f.find('a')
                text_or_title = anchor.get('title') if anchor.get('title') else anchor.get_text()
                found.append((text_or_title, anchor['href']))
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
    message_html = ''
    if found_word:
        for f in found_word:
            message_html += '<h3>' + f[0] + '</h3>'
            link = '<a clicktracking="off" href="' + f[1] + '">'
            message_html += link + f[1] + '</a>'
        if message_html:
            success_message = 'Great news! We found results in your search for ' \
                              '"{}" at {}\n'.format(search_word, url)
            success_message += message_html
            send_mail(email_address, search_word, success_message)
    else:
        message_html += '<h3>No Results</h3>'
        message_html += '<p>No results were found for the following input</p>'
        search_input = '<p>url: ' + url + '</p>'
        search_input += '<p>keyword: ' + search_word + '</p>'
        search_input += '<p>element type: ' + elem_type + '</p>'
        search_input += '<p>element attribute descriptor: ' + elem_attr + '</p>'
        final_bit = '<p>Either the keyword is not present or there is an issue with the provided input.'
        message_html += search_input
        message_html += final_bit
        send_mail(email_address, search_word, message_html)
