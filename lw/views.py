from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .crawl import collect  # TODO remove this when CRON task is added to crawl.p as below
# Create your views here.


def index(request):
    template = loader.get_template('home.html')


# TODO This block will move into a CRON task at bottom of crawl.py. It is in views for
# now to fire when loading the page for testing purposes
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

    return HttpResponse(template.render())

