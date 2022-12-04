import requests
from bs4 import BeautifulSoup
import re


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

