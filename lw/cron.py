from .crawl import collect
from .mail import send_mail


def trigger():
    # moved from views.py
    # TODO url, search_word, div_id, and user should come from search table of database
    # TODO past_hits should come from results table of database
    url = 'https://prodogsdirect.org.uk/category/dogs/'
    search_word = 'Bulldog'
    div_id = 'entry-summary'
    user = 'brianmcdowell@ufl.edu'
    past_hits = []
    results_html = ''

    found_word = collect(url, search_word, div_id)
    if found_word:
        for f in found_word:
            if f not in past_hits:
                results_html += f[0] + '\n'
                results_html += f[1] + '\n'
        if results_html:
            success_message = 'Great news! We found new results in your search for ' \
                              '"{}" at {}\n'.format(search_word, url)
            success_message += results_html
            send_mail(user, search_word, success_message)
