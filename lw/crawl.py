import requests
from bs4 import BeautifulSoup
import re


def collect(url, search_word, div_id):
    """
    This function performs the webscraping for the project.
    Called from cron.py and views.py
    """
    try:
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        body = soup.body

        divs = body.find_all('div', attrs={'class', div_id})
        found = []
        for d in divs:
            if d.find_all('p', string=re.compile(search_word)):
                anchor = d.find('a')
                found.append((anchor.get('title'), anchor['href']))
                # found.append((anchor['href'], anchor.get('title')))
                # the old way. Delete once the new way works

        return found
    except Exception as e:
        print(e)
        return False

