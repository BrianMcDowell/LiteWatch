import requests
from bs4 import BeautifulSoup
import re


def collect(url, search_word, div_id):
    try:
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        body = soup.body

        divs = body.find_all('div', attrs={'class', div_id})
        found = []
        for d in divs:
            if d.find_all('p', string=re.compile(search_word)):
                anchor = d.find('a')
                found.append((anchor['href'], anchor.get('title')))
        return found
    except Exception as e:
        print(e)
        return False

# TODO write CRON task here to collect search criteria from DB and run collect above
# this will include evaluating past hits to determine if any new hits are reportable