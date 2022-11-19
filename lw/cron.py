from .crawl import collect


def trigger():
    # moved from views.py
    # TODO url, search_word, div_id, and user should come from search table of database
    # TODO past_hits should come from results table of database
    url = 'https://prodogsdirect.org.uk/category/dogs/'
    search_word = 'Bulldog'
    div_id = 'entry-summary'
    user = ''
    past_hits = []

    found_word = collect(url, search_word, div_id)
    if found_word:
        for f in found_word:
            if f not in past_hits:
                print(f)  # TODO this will change to "report hit to database"
                # currently outputs to text file at var/mail/brianmcdowell